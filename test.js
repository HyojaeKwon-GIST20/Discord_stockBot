const Discord = require('discord.js');
const client = new Discord.Client();

client.on('ready', () => {
	console.log(`Logged in as ${client.user.tag}!`);
});

//'주식거래'를 보내면 '하지마'로 응답
client.on('interaction', async interaction => {
	if (!interaction.isCommand()) return;
	if (interaction.commandName === '주식 거래') {
		await interaction.reply('하지마!');
	}
});

client.login('token'); 
//당신 봇의 토큰을 입력하세요