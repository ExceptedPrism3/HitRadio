const { ActivityType } = require('discord.js');
const config = require('../config.json');
const { loadCommands } = require("../loaders/commandLoader");

module.exports = {
    name: 'ready',
    once: true,
    execute(client) {
        console.log(`Logged in as ${client.user.tag}!`);

        loadCommands(client);

        let index = 0;
        const statusMessages = config.statusMessages;
        const intervalSeconds = config.statusInterval * 1000;

        setInterval(() => {
            if (index >= statusMessages.length) {
                index = 0; // Reset to the first message if we've gone through all of them
            }
            client.user.setActivity(statusMessages[index], { type: ActivityType.Listening });
            index++;
        }, intervalSeconds);
    },
};
