const { SlashCommandBuilder } = require('discord.js');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('help')
        .setDescription('❓ Get a list of all commands.'),
    async execute(interaction) {
        // Dynamically get all commands
        const commands = interaction.client.commands.map(command => `\`/${command.data.name}\` - ${command.data.description}`).join('\n');

        const embed = {
            color: 65280,
            title: '❓ Help - List of Commands',
            description: commands,
        };

        await interaction.reply({ embeds: [embed], ephemeral: true });
    },
};
