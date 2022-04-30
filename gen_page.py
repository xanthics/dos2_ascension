from browser import document as doc
from browser.html import TABLE, TR, TH, TD, INPUT, SELECT, SECTION, DIV, OPTION, BR, COL, H1, BUTTON, P, UL, LI, STRONG, H2, A
from json import load
from collections import defaultdict
import re
from artifact_data import artifacts


def min_search_coverage(items):
	pattern = re.compile('[^a-z ]')
	t_str = ' '.join(items).lower()
	clean = pattern.sub('', t_str).split()
	ret = []
	sorted_clean = sorted(clean, key=len)
	for idx, word in enumerate(sorted_clean, start=1):
		if not any(word in x for x in sorted_clean[idx:]):
			ret.append(word)
	return ' '.join(ret)


def init_notes():
	# Basic Ascension notes
	s = SECTION(A("C+P from offical docs on 2021/09/03", href="https://docs.google.com/document/d/1du5jE2dyDE4B4-Za0wolfe50ReeKXqkqdgG5FvAwKTo/edit#heading=h.2xtj3l28uhgr") +
				BR() +
				P("While Ascension provides many bonuses in terms of basic statistical increases (bonus resistances, Attributes, Abilities, etc.), the various “keywords” it grants represent a significant contribution to character build diversification. Ascension keywords generally function like complex Talents that provide a character with some sort of ability that deeply impacts their mode of play (these effects allow the creation of character builds in the true sense, not just different loadouts). Keywords generally provide a base effect that further investment builds upon with various mutators or additional activation conditions. Below you will find a list of the base effects of the available Ascension keywords."), Class='keyword')

	l_items = [
		["Abeyance:",
		 "When Abeyance activates, it instantly heals whatever damage it activated from; at the start of your next turn, suffer that amount +15% as unresistable damage, split evenly between your armors and Vitality. Any remaining damage to armor is instead dealt to Vitality.",
		"Basic activation: If it is not your turn, when you are dealt combat damage equivalent to at least 30% of your maximum Vitality (-0.5% per Inertia or Form embodied, minimum of 20%) at once, Abeyance activates."],
		["Adaptation:",
		"When Adaptation is activated, gain or lose up to 30% of your maximum Physical or Magic Armor until their current values equilibrate; loss occurs from the higher of the two values and restoration occurs to the lower of the two values. Additionally, gain a stacking Adaptation status, which lasts for 1 turn, stacks up to 10 and grants +2.5% to FIN, CON, POW, and WIT per stack."
		"Adaptation skill: 1 AP, no cooldown, activate Adaptation when cast."],
		["Benevolence:",
		"When Benevolence is activated, remove 2 stacks of Battered and Harried from the target and move half these stacks (rounded up) onto yourself. Restore 5% of your missing Vitality per stack of Battered or Harried removed this way.",
		"Gain Mercy, 2 AP, 1 turn cooldown, activate Benevolence on each ally within 8m."],
		["Celestial:",
		"1 AP reaction that restores 15% of target's Vitality (+2% per Life embodied).",
		"This is a Reaction: Reactions are performed automatically when their conditions are satisfied, and can only be performed when it is not the reacting character's turn."],
		["Centurion:",
		"1 AP reaction that performs a basic attack on a target within weapon range.",
		"This is a Reaction: Reactions are performed automatically when their conditions are satisfied, and can only be performed when it is not the reacting character's turn."],
		["Defiance:",
		"When you become Flanked, and when you start your turn within 5m of at least two enemies, Defiance activates for 1 turn."],
		["Elementalist:",
		"1 AP reaction, deals elemental damage to all characters within 2m of the reaction's target. When you perform an Elementalist reaction, suffer damage of the reaction's type, equivalent to 10% of your maximum Vitality for each stack of Elementalist you have. Then gain 1 stack of Elementalist, or 2 if using the same element twice in a row.",
		"This is a Reaction: Reactions are performed automatically when their conditions are satisfied, and can only be performed when it is not the reacting character's turn."],
		["Occultist:",
		"1 AP reaction, apply Bane for 2 turns. Bane deals Physical damage to the target at the beginning of their turn. When Bane ends, it deals its base damage +5% per Battered or Harried that the target suffered over its duration.",
		"This is a Reaction: Reactions are performed automatically when their conditions are satisfied, and can only be performed when it is not the reacting character's turn."],
		["Paucity:",
		"While active, Paucity grants +15% lifesteal (+2% per Entropy).",
		"Basic activation: Once per round, when you drop to 25% Vitality or below, activate Paucity."],
		["Predator:",
		"1 AP reaction that performs a basic attack on a target within weapon range. If this attack is performed with a melee weapon, it has +30% critical chance. Additionally, if this attack is performed with a dagger, attempt to sneak afterward.",
		"This is a Reaction: Reactions are performed automatically when their conditions are satisfied, and can only be performed when it is not the reacting character's turn."],
		["Presence:",
		"Presence is considered active on any allies that are affected by your Leadership."],
		["Prosperity:",
		"Basic activation: When you have at least 90% Vitality (-1% per Form or Life embodied), Prosperity is considered active."],
		["Purity:",
		"When Purity is activated, instantly heal 15% (+1.5% per Life embodied) of missing Vitality and armors - also gain a 10m radius aura for 2 turns that restores 8% (+1.5% per Life embodied) of missing Vitality, Magic, and Physical Armor per turn to yourself and allies. 4 turn Cooldown.",
		"Basic activation: When reduced to 30% Vitality (+1.5% per Life embodied) or below, activate Purity."],
		["Violent Strike:",
		"If Violent Strike is active when you use a skill, basic attack or reaction, perform a Violent Strike on the first enemy you hit, which deals 30% of your weapon damage to enemies within 2m of that target."],
		["Vitality Void:",
		"When Vitality Void is activated, deal piercing damage, split between all enemies within 3m of you, equal to 11% of your maximum Vitality (+1% per Entropy embodied), and you heal for 15% (+2% per Entropy embodied) of this damage. Vitality Void is not affected by increases or reductions to your damage.",
		"Basic activation: Whenever you spend a Source Point in combat, activate Vitality Void."],
		["Volatile Armor:",
		"Whenever you suffer damage to armor of the designated type, deal the listed percentage of that damage to all characters within range, as whatever damage type is noted."],
		["Voracity:",
		"Whenever an enemy dies in combat, your Voracity effects are granted to you. If the dying enemy was a summon, you are instead granted only 20% of these effects' intended values."],
		["Ward:",
		"When Ward is active, gain +10% to all resistances.",
		"Basic activation: After you have suffered total damage exceeding 60% of your total Vitality (-0.5% per Constitution over 10, minimum of 20%), activate Ward for 1 turn."],
		["Wither:",
		"Withered reduces the effect of Power by 15% (+2% per your Entropy embodied). Additionally, once per round per target, Wither applies 1 Battered and Harried as it is applied."]
	]

	for li in l_items:
		s <= H2(li[0]) + UL(LI(x) for x in li[1:])
#	doc['notes'] <= s

	# Note about Pip and Derpy mod changes
	pip_generic = [
		"<strong>Any note in this color is specific to Pip's Mod.</strong>  Current as of 2021/09/12.",
		"Opportunist grants 2 free generic reaction charges, up from 1",
		"""Added a way to recycle Artifacts into new ones; dismantling Artifacts gives you a special item. Consume 2 of them to receive a new Artifact, scaled to your level.<br />
An old idea that Ameranth had ages ago which I liked. Newbies immediately recycling artifacts that don't fit their current builds would be a concern with this function, but I don't imagine new players will be playing my patch.""",
		"""Made Centurion on-miss activators have no range limit for range weapons, but activations are limited to 1 per round this way<br />
No height range bonus is applied.<br />
Apparently, these nodes also work when blocking with a shield. The more you know!""",
		"Elementalist inflicts half as much self-damage, and deals 110% damage, up from 90%. DR made the self-damage decrease very justifiable.",
		"""Made all infused reactions (except for Nymph SP transfer, Ritual and Celestial resurrect) refund their SP cost<br />
Another band-aid fix; this will not fix their damage issues, but it should make the infused reactions that apply tiered effects or other statuses a nice option, if you're willing to bank 1 SP to use them. Centurion Ruptured Tendons node might become particularly pog."""
	]
	derpy_generic = [
		"<strong>Any note in this color is specific to Derpy's Mod.</strong>  Current as of 2022/04/29.",
		"You can also search for derpy to see only his changed nodes.",
		"""Elementalist: Removed self damage and lowered multiplier from 90 to 70<br />
Spellcaster's Finesse: Now also works on Polymorph skills and doesn't remove Finesse's AP recovery effect anymore<br />
Paucity: Default duration from 1 turn to 2 turns<br />
Defiance: Default duration from 1 turn to 2 turns, Now also activates at the end of your turn if you are within 5m of at least two enemies<br />
Mercy: Radius from 8m to 13m<br />
Purity: Added back the Purity aura owner icon, Changed Purity Cooldown icon so it's easier to differentiate between them<br />
Vitality Void: Changed damage to Physical from Piercing
""",
		"""<strong>T1 Nodes</strong><br />
Ascension nodes that previously granted the Inconspicuous talent have been replaced with Opportunist for 2 turns, and now apply up to Subjugated II to every enemy within 5m of yourself. They also require to be in combat<br />
Ascension nodes that previously granted the Pawn talent have been replaced with Escapist for 2 turns. They also require to be in combat<br />
Casting Escapist -> Weapon skill will refresh Escapist CD. This is intended<br />
Ascension nodes that previously granted the Savage Sortilege talent have been increased from 1 turn to 3 turns. They also require to be in combat"""
	]

	s = SECTION(Class='pip')
	for d in pip_generic:
		s <= P(d)
	doc['notes'] <= s
	s = SECTION(Class='derpy')
	for d in derpy_generic:
		s <= P(d)
	doc['notes'] <= s


def init_page():
	init_notes()
	# keep track of ascendancy resources needed/granted
	# set up page search functions
	always_show = SELECT(Id=f"always_show", Class=f"filter onehundred")
	for s in ['no', 'yes']:
		always_show <= OPTION(s.capitalize(), value=s)

	t = TABLE(TR(TH() + TH('Selection')))
	t <= TR(TD("Only Show Selected Ascendancies:", Class="right_text") + TD(always_show))
	t <= TR(TD("Keyword(s) Search:", Class="right_text") + TD(INPUT(Type='text', Id="keywords", Class='filter') + BUTTON('x', Id='clear_keywords')))
	doc['filter'] <= t

	# set up ascendancies
	with open('node_data.json', 'r') as f:
		data = load(f)
	nodes = defaultdict(list)
	for domain in ['Special', 'Force', 'Entropy', 'Form', 'Inertia', 'Life']:
		s = SECTION(H1(domain), Id=domain.lower(), Class=domain.lower())
		for item in data[domain]:
			select_id = f'{item["name"].replace(" ", "_")}'
			data_value = min_search_coverage([item['name']] + [z for x in item['nodes'] for y in x for z in y] + [y for x in item['implicit'] for y in x if y] + ([item['special']] if 'special' in item else []))
			t = TABLE(COL(Class='first_column') + COL() + COL(), Class='onehundred borders', Id=select_id, data_value=data_value, data_points=len(item['nodes']))
			t <= TR(TH(INPUT(type='checkbox', Id=f'c-{select_id}', Class="save")) + TH(item['name']) + TH(f"Tier {item['tier']}"))
			req = ', '.join([f"{item['require'][x]} {x}" for x in item['require']])
			comp = ', '.join([f"{item['complete'][x]} {x}" for x in item['complete']]) if item['complete'] else 'None'
			t <= TR(TH() + TH(f"Required: {req}") + TH(f"Completion: {comp}"))
			if len(item['nodes']):
				t <= TR(TH('Selection') + TH('Value(s)') + TH('Implicit(s)'))
				for c in range(len(item['nodes'])):
					if not item['nodes'][c]:
						item['nodes'][c].append(['Nothing'])
					rspan = len(item['nodes'][c])
					n = ', '.join(item['nodes'][c][0])
					nodes[n].append((domain, item['name'], c+1, 1))
					if item['implicit'][c]:
						nodes[', '.join(item['implicit'][c])].append((domain, item['name'], c+1))
					t <= TR(TD(f"{c+1}: " + SELECT((OPTION(x, value=f"{x}") for x in ['Any'] + list(range(1, rspan+1))), Id=f'{select_id}{c}', Class='save'), rowspan=rspan) + TD(DIV(n, Id=f'{select_id}{c}{1}', data_content=min_search_coverage(item['nodes'][c][0] + [item['name']]))) + TD(DIV(', '.join(item['implicit'][c]), data_content=min_search_coverage(item['implicit'][c])), rowspan=rspan))
					for idx in range(1, len(item['nodes'][c])):
						n = ', '.join(item['nodes'][c][idx])
						nodes[n].append((domain, item['name'], c+1, idx+1))
						t <= TR(TD(DIV(n, Id=f'{select_id}{c}{idx + 1}', data_content=min_search_coverage(item['nodes'][c][idx] + [item['name']]))))
			if 'special' in item:
				t <= TR(TD(DIV(item['special'], data_content=min_search_coverage([item['special']] + [item['name']])), colspan=3))
				nodes[item['special']].append((domain, item['name'], 0))
			t <= TR(TH(item['flavor'], colspan=3))
			s <= t
		doc['ascensions'] <= s

	# add core nodes
	for c_node in ['Force', 'Entropy', 'Form', 'Inertia', 'Life']:
		t = TABLE(COL(Class='first_column') + COL() + COL(), Class='onehundred borders', data_value=f"core {c_node.lower()}", Id=f"Core_{c_node}", data_points=1)
		t <= TR(TH(INPUT(type='checkbox', Id=f'c-Core_{c_node}', Class="save")) + TH(f"Core: {c_node}") + TH(f"Tier 0"))
		t <= TR(TH() + TH(f"Required: None") + TH(f"Completion: 1 {c_node}"))
		t <= TR(TH("One of the 5 central nodes.", colspan=3))
		doc['special'] <= t
	# set up artifacts
	for domain in ["Weapon", "Armor", "Jewelry"]:
		s = SECTION(H1(domain), Id=domain.lower(), Class=domain.lower())
		for item in artifacts[domain]:
			nodes[item['power']].append((domain, item['name'], item['type']))
			select_id = f'{item["name"].replace(" ", "_")}'
			data_value = min_search_coverage([item['name']] + [item['power']] + [item['notes']])
			t = TABLE(COL(Class='first_column') + COL(Class='second_column') + COL(), Class='onehundred borders', Id=select_id, data_value=data_value, data_points=0)
			t <= TR(TH(INPUT(type='checkbox', Id=f'c-{select_id}', Class="save")) + TH(item['name']) + TH(item['tier']))
			t <= TR(TH(item['type']) + TD(item['power'], rowspan=2) + TD(f"Artifact Power: {item['artifact']}" if item['artifact'] else ' '))
			t <= TR(TH(item['subtype']) + TD(f"Rune Power: {item['rune']}" if item['rune'] else ' '))
			if item['notes']:
				t <= TR(TH(item['notes'], colspan=3))
			t <= TR(TD() + TH(item['flavor']) + TD())
			s <= t
		doc['artifacts'] <= s

	# set up modifiers list
	t = TABLE(COL(Class='node_column') + COL(), Class='onehundred borders')
	t <= TR(TH("Modifier") + TH('Location(s)'))
	for node in sorted(nodes):
		data_value = min_search_coverage(node.split())
		t <= TR(TD(DIV(node), rowspan=len(nodes[node])) + TD(f"{nodes[node][0][1]}: {nodes[node][0][2]}{'.' + str(nodes[node][0][3]) if len(nodes[node][0]) == 4 else ''}", Class=nodes[node][0][0].lower()), data_value=data_value)
		for idx in range(1, len(nodes[node])):
			t <= TR(TD(f"{nodes[node][idx][1]}: {nodes[node][idx][2]}{'.' + str(nodes[node][idx][3]) if len(nodes[node][idx]) == 4 else ''}", Class=nodes[node][idx][0].lower()), data_value=data_value)

	doc['modifiers'] <= SECTION(t)

	# working on
	notes = [
		'Move select/search to a floating bar'
	]
	s = SECTION(P(x) for x in notes)
	doc['todo'] <= s


init_page()
doc['loading'] <= DIV(Id='prerendered')
