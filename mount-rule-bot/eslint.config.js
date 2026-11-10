/**
 * ESLint flat configuration for the Mount rules bot.
 * @module eslint.config
 */

// Third-party modules
import js from '@eslint/js';
import eslintConfigPrettier from 'eslint-config-prettier/flat';
import globals from 'globals';

export default [
    {
        ignores: ['node_modules/', 'images/'],
    },
    js.configs.recommended,
    {
        files: ['**/*.js'],
        languageOptions: {
            ecmaVersion: 'latest',
            sourceType: 'module',
            globals: {
                ...globals.node,
            },
        },
        rules: {
            'no-console': 'off',
        },
    },
    eslintConfigPrettier,
];
