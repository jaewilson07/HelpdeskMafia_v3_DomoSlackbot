import { registerListeners } from './listeners';

async function startBot() {
    // Initialize Slackbot
    // Add initialization logic here, e.g., setting up Slack client

    // Register listeners (commands, events, etc.)
    registerListeners();

    // Start the bot
    // Add logic to start the bot, e.g., listening for events
}

startBot();