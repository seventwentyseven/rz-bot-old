# How 2
Put this into constants/commands.py after _help command in your gulag. You can see how we implemented it in our seventwentyseven/gulag repo.

```python
@command(Privileges.Normal, hidden=True)
async def _link(ctx: Context) -> str:
	"""Link your osu account on our discord server"""
	discordtag = " ".join(ctx.args[0:])
	if not discordtag:
		return f'Please enter your discord tag.\nExample usage: !link def750#0947'

	#Check if on chat
	if ctx.recipient is not glob.bot:
		return f'Command only available in DMs with {glob.bot.name}.'
	randcode = random.randrange(10000, 99999)

	if not await glob.db.fetch('SELECT osu_id FROM discord WHERE osu_id = %s', [ctx.player.id]):
		await glob.db.execute(
			'INSERT INTO discord '
			'(osu_id, discord_tag, code) '
			'VALUES (%s, %s, %s)',
			[ctx.player.id, discordtag, randcode]
    )
	else:
		await glob.db.execute(
			'UPDATE discord '
			'SET osu_id = %s, discord_tag = %s, code = %s '
			'WHERE osu_id = %s',
			[ctx.player.id, discordtag, randcode, ctx.player.id]
		)
	print(f"<{ctx.player.name} ({ctx.player.id})> Executed link command, discord tag specified: {discordtag}, code recieved: {randcode}")
	return f"Your verification code: {randcode} \nDiscord Tag you specified: {discordtag} \nIf it's incorrect please execute command again ;)"
```