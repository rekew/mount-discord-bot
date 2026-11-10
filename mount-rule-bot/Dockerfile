FROM node:24-slim

ENV NODE_ENV=production

RUN npm install --global pnpm@11.28.11

WORKDIR /app

COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY main.js ./
COPY src ./src
COPY scripts ./scripts
COPY images ./images

RUN useradd --create-home --uid 10001 bot && chown -R bot:bot /app
USER bot

CMD ["pnpm", "start"]
