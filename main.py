import os
import discord
from discord.ext import commands


# =========================
# CONFIGURATION
# =========================

TOKEN = os.getenv("TOKEN")

CREATE_CHANNEL_ID = 1567149900972560465
CATEGORY_ID = 1567149899454087211
PANEL_CHANNEL_ID = 1567150052902699218

ROOM_TOPIC_PREFIX = "MOUNT_ROOM_OWNER="
PANEL_MARKER = "mount-bot-control-panel"

ROOM_OWNERS = {}


# =========================
# BOT SETUP
# =========================

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


# =========================
# HELPERS
# =========================

def get_room_owner_id(channel):
    if not channel:
        return None

    return ROOM_OWNERS.get(channel.id)


async def get_owned_room(interaction):
    """Find the voice room belonging to the user who clicked the button."""

    if not interaction.user.voice or not interaction.user.voice.channel:
        await interaction.response.send_message(
            "❌ Сначала зайдите в свою голосовую комнату.",
            ephemeral=True
        )
        return None

    channel = interaction.user.voice.channel
    owner_id = get_room_owner_id(channel)

    if owner_id != interaction.user.id:
        await interaction.response.send_message(
            "❌ Вы не являетесь владельцем этой комнаты.",
            ephemeral=True
        )
        return None

    return channel


# =========================
# RENAME MODAL
# =========================

class RenameModal(discord.ui.Modal, title="Переименовать комнату"):

    new_name = discord.ui.TextInput(
        label="Новое название комнаты",
        placeholder="Введите название...",
        max_length=100
    )

    async def on_submit(self, interaction: discord.Interaction):

        channel = await get_owned_room(interaction)
        if channel is None:
            return

        await channel.edit(name=self.new_name.value)

        await interaction.response.send_message(
            f"✅ Название комнаты изменено на **{self.new_name.value}**.",
            ephemeral=True
        )


# =========================
# USER LIMIT MODAL
# =========================

class LimitModal(discord.ui.Modal, title="Изменить лимит участников"):

    limit = discord.ui.TextInput(
        label="Количество участников (0 — без ограничений)",
        placeholder="Например: 5",
        max_length=2
    )

    async def on_submit(self, interaction: discord.Interaction):

        channel = await get_owned_room(interaction)
        if channel is None:
            return

        try:
            limit = int(self.limit.value)

            if limit < 0 or limit > 99:
                raise ValueError

        except ValueError:
            await interaction.response.send_message(
                "❌ Введите число от 0 до 99.",
                ephemeral=True
            )
            return

        await channel.edit(user_limit=limit)

        if limit == 0:
            message = "✅ Лимит участников отключён."
        else:
            message = f"✅ Лимит комнаты установлен: **{limit}**."

        await interaction.response.send_message(
            message,
            ephemeral=True
        )


# =========================
# KICK SELECT
# =========================

class KickSelect(discord.ui.Select):

    def __init__(self, room):

        self.room_id = room.id

        options = []

        for member in room.members:
            if member.bot:
                continue

            owner_id = get_room_owner_id(room)

            if member.id == owner_id:
                continue

            options.append(
                discord.SelectOption(
                    label=member.display_name[:100],
                    value=str(member.id)
                )
            )

        super().__init__(
            placeholder="Выберите участника...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        room = interaction.guild.get_channel(self.room_id)

        if room is None:
            await interaction.response.send_message(
                "❌ Комната больше не существует.",
                ephemeral=True
            )
            return

        owner_id = get_room_owner_id(room)

        if owner_id != interaction.user.id:
            await interaction.response.send_message(
                "❌ Вы не являетесь владельцем этой комнаты.",
                ephemeral=True
            )
            return

        member_id = int(self.values[0])
        member = interaction.guild.get_member(member_id)

        if member is None or not member.voice:
            await interaction.response.send_message(
                "❌ Участник больше не находится в голосовом канале.",
                ephemeral=True
            )
            return

        if member.voice.channel.id != room.id:
            await interaction.response.send_message(
                "❌ Этот участник уже покинул вашу комнату.",
                ephemeral=True
            )
            return

        # Deny access to this particular voice room.
        overwrite = room.overwrites_for(member)
        overwrite.connect = False

        await room.set_permissions(
            member,
            overwrite=overwrite,
            reason=f"Участник ограничен владельцем комнаты {interaction.user}"
        )

        # Disconnect the member after applying the restriction.
        await member.move_to(
            None,
            reason="Отключён владельцем голосовой комнаты"
        )

        await interaction.response.send_message(
            f"✅ **{member.display_name}** отключён от комнаты и больше не сможет подключиться к ней.",
            ephemeral=True
        )


class KickView(discord.ui.View):

    def __init__(self, room):
        super().__init__(timeout=60)
        self.add_item(KickSelect(room))


# =========================
# MAIN CONTROL PANEL
# =========================

class VoiceControlView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Переименовать",
        emoji="✏️",
        style=discord.ButtonStyle.primary,
        custom_id="mount_rename"
    )
    async def rename(self, interaction, button):

        channel = await get_owned_room(interaction)
        if channel is None:
            return

        await interaction.response.send_modal(RenameModal())

    @discord.ui.button(
        label="Исключить участника",
        emoji="🚫",
        style=discord.ButtonStyle.danger,
        custom_id="mount_kick"
    )
    async def kick(self, interaction, button):

        channel = await get_owned_room(interaction)
        if channel is None:
            return

        if len([m for m in channel.members if not m.bot and m.id != interaction.user.id]) == 0:
            await interaction.response.send_message(
                "В вашей комнате сейчас нет других участников.",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            "Выберите участника, которому нужно запретить вход в эту комнату:",
            view=KickView(channel),
            ephemeral=True
        )

    @discord.ui.button(
        label="Лимит участников",
        emoji="👥",
        style=discord.ButtonStyle.secondary,
        custom_id="mount_limit"
    )
    async def limit(self, interaction, button):

        channel = await get_owned_room(interaction)
        if channel is None:
            return

        await interaction.response.send_modal(LimitModal())

    @discord.ui.button(
        label="Приватность",
        emoji="🔒",
        style=discord.ButtonStyle.success,
        custom_id="mount_privacy"
    )
    async def privacy(self, interaction, button):

        channel = await get_owned_room(interaction)
        if channel is None:
            return

        everyone = interaction.guild.default_role
        overwrite = channel.overwrites_for(everyone)

        is_private = (
            overwrite.connect is False
            or overwrite.view_channel is False
        )

        if is_private:
            overwrite.view_channel = True
            overwrite.connect = True

            await channel.set_permissions(
                everyone,
                overwrite=overwrite
            )

            message = "🔓 Комната теперь открыта для всех."
        else:
            overwrite.view_channel = False
            overwrite.connect = False

            await channel.set_permissions(
                everyone,
                overwrite=overwrite
            )

            message = "🔒 Комната теперь приватная."

        await interaction.response.send_message(
            message,
            ephemeral=True
        )


# =========================
# PANEL EMBED
# =========================

def create_panel_embed():

    embed = discord.Embed(
        title="🎙️ Управление голосовой комнатой",
        description=(
            "Зайдите в свою голосовую комнату, чтобы управлять ею.\n\n"
            "✏️ **Переименовать** — изменить название комнаты.\n"
            "🚫 **Исключить участника** — отключить участника и запретить ему повторный вход.\n"
            "👥 **Лимит участников** — установить ограничение на количество участников.\n"
            "🔒 **Приватность** — закрыть или открыть комнату.\n\n"
            "Команды управления доступны только владельцу комнаты."
        ),
        color=discord.Color.blurple()
    )

    embed.set_footer(text=PANEL_MARKER)

    return embed


# =========================
# STARTUP PANEL
# =========================

async def create_or_update_panel():

    channel = await bot.fetch_channel(PANEL_CHANNEL_ID)

    if not isinstance(channel, discord.TextChannel):
        print("ERROR: PANEL_CHANNEL_ID is not a text channel.")
        return

    embed = create_panel_embed()
    view = VoiceControlView()

    # Find the previous panel to avoid creating duplicates after restarts.
    async for message in channel.history(limit=100):

        if message.author.id != bot.user.id:
            continue

        if not message.embeds:
            continue

        footer = message.embeds[0].footer.text

        if footer == PANEL_MARKER:
            await message.edit(
                embed=embed,
                view=view
            )
            print("Control panel updated.")
            return

    await channel.send(
        embed=embed,
        view=view
    )

    print("Control panel sent.")


# =========================
# BOT STARTUP
# =========================

class MountBot(commands.Bot):

    async def setup_hook(self):

        # Register persistent buttons so old panel buttons work after restart.
        self.add_view(VoiceControlView())

        try:
            await create_or_update_panel()
        except Exception as error:
            print(f"Could not create control panel: {error}")


bot = MountBot(
    command_prefix="!",
    intents=intents
)


# =========================
# TEMPORARY ROOM CREATION
# =========================

@bot.event
async def on_voice_state_update(member, before, after):

    # Create a room when someone joins the designated channel.
    if after.channel and after.channel.id == CREATE_CHANNEL_ID:

        category = member.guild.get_channel(CATEGORY_ID)

        if category is None:
            print("ERROR: Voice category not found.")
            return

        try:
            room = await member.guild.create_voice_channel(
                name=f"Комната {member.display_name}",
                category=category,
                reason="Создание временной голосовой комнаты"
            )

            ROOM_OWNERS[room.id] = member.id

            await member.move_to(room)

            print(f"Created room for {member.display_name}")

        except discord.Forbidden:
            print("ERROR: Bot does not have permission to create or move members.")

        except discord.HTTPException as error:
            print(f"ERROR creating room: {error}")

    # Delete an empty temporary room.
    if before.channel:

        old_channel = before.channel

        if get_room_owner_id(old_channel) is not None:
            if len(old_channel.members) == 0:

                try:
                    await old_channel.delete(
                        reason="Временная голосовая комната пуста"
                    )
                    print(f"Deleted empty room: {old_channel.name}")

                except discord.HTTPException as error:
                    print(f"Could not delete room: {error}")
                    
@bot.event
async def on_message(message):

    if message.author.bot:
        return

    print(
        f"[MESSAGE RECEIVED] {message.author}: {message.content}",
        flush=True
    )

    await bot.process_commands(message)

@bot.command(name="clear")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 10):

    if amount < 1 or amount > 100:
        print("IF TRIGGERED: Invalid amount", flush=True)
        await ctx.send("Invalid amount.")
        return

    print("IF PASSED: Amount is valid", flush=True)

    deleted = await ctx.channel.purge(limit=amount + 1)

    print(f"Deleted: {len(deleted) - 1}", flush=True)

    message = await ctx.send(
        f"✅ Deleted {len(deleted) - 1} messages."
    )
    await message.delete(delay=3)


@clear.error
async def clear_error(ctx, error):

    print(f"[CLEAR ERROR] {type(error).__name__}: {error}")

    if isinstance(error, commands.MissingPermissions):
        print("[CLEAR] User does not have Manage Messages permission")
        await ctx.send("❌ You need Manage Messages permission.")

    elif isinstance(error, commands.BadArgument):
        print("[CLEAR] Invalid command argument")
        await ctx.send("❌ Please provide a valid number.")

    else:
        print("[CLEAR] Unexpected error occurred")
        raise error

# =========================
# RUN
# =========================

if not TOKEN:
    raise RuntimeError(
        "DISCORD_TOKEN is missing. Set it as an environment variable."
    )

bot.run(TOKEN)