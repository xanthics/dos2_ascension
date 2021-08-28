from browser import document as doc
from browser.html import TABLE, TR, TH, TD, INPUT, SELECT, SECTION, DIV, OPTION, BR, COL, H1, BUTTON, P
from json import load
from collections import defaultdict
import re


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


def init_page():
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
			data_value = min_search_coverage([item['name']] + [z for x in item['nodes'] for y in x for z in y] + [y for x in item['implicit'] for y in x if y])
			t = TABLE(COL(Class='first_column') + COL() + COL(), Class='onehundred borders', data_value=data_value, data_asc_id=item["name"].replace(" ", "_"))
			t <= TR(TH(INPUT(type='checkbox', Id=f'c-{item["name"].replace(" ", "_")}', Class="save")) + TH(item['name']) + TH(f"Tier {item['tier']}"))
			req = ', '.join([f"{item['require'][x]} {x}" for x in item['require']])
			comp = ', '.join([f"{item['complete'][x]} {x}" for x in item['complete']]) if 'complete' in item else 'Nothing'
			t <= TR(TH() + TH(f"Required: {req}") + TH(f"Completion: {comp}"))
			if len(item['nodes']):
				t <= TR(TH('Selection') + TH('Value(s)') + TH('Implicit(s)'))
				for c in range(len(item['nodes'])):
					rspan = len(item['nodes'][c])
					n = ', '.join(item['nodes'][c][0])
					nodes[n].append((domain, item['name'], c, 0))
					if item['implicit'][c]:
						nodes[', '.join(item['implicit'][c])].append((domain, item['name'], c))
					t <= TR(TD(f"{c+1}: " + SELECT((OPTION(x, value=f"{x}") for x in ['Any'] + list(range(1, rspan+1))), Id=f'{item["name"].replace(" ", "_")}{c}', Class='save'), rowspan=rspan) + TD(DIV(n, Id=f'{item["name"].replace(" ", "_")}{c}{1}', data_content=min_search_coverage(item['nodes'][c][0] + [item['name']]))) + TD(DIV(', '.join(item['implicit'][c]), data_content=min_search_coverage(item['implicit'][c])), rowspan=rspan))
					for idx in range(1, len(item['nodes'][c])):
						n = ', '.join(item['nodes'][c][idx])
						nodes[n].append((domain, item['name'], c, idx))
						t <= TR(TD(DIV(n, Id=f'{item["name"].replace(" ", "_")}{c}{idx + 1}', data_content=min_search_coverage(item['nodes'][c][idx] + [item['name']]))))
			t <= TR(TH(item['flavor'], colspan=3))
			s <= t
		doc['ascensions'] <= s

	# add core nodes
	for c_node in ['Force', 'Entropy', 'Form', 'Inertia', 'Life']:
		t = TABLE(COL(Class='first_column') + COL() + COL(), Class='onehundred borders', data_value=c_node, data_asc_id=f"Core_{c_node}")
		t <= TR(TH(INPUT(type='checkbox', Id=f'c-Core_{c_node}', Class="save")) + TH(f"Core: {c_node}") + TH(f"Tier 0"))
		t <= TR(TH() + TH(f"Required: None") + TH(f"Completion: 1 {c_node}"))
		t <= TR(TH("One of the 5 central nodes.", colspan=3))
		doc['special'] <= t
	# set up nodes list
	t = TABLE(COL(Class='node_column') + COL(), Class='onehundred borders')
	t <= TR(TH("Node") + TH('Location(s)'))
	for node in sorted(nodes):
		data_value = min_search_coverage(node.split())
		t <= TR(TD(node, rowspan=len(nodes[node])) + TD(f"{nodes[node][0][1]}: {nodes[node][0][2]}{'.' + str(nodes[node][0][3]) if len(nodes[node][0]) == 4 else ''}", Class=nodes[node][0][0].lower()), data_value=data_value)
		for idx in range(1, len(nodes[node])):
			t <= TR(TD(f"{nodes[node][idx][1]}: {nodes[node][idx][2]}{'.' + str(nodes[node][idx][3]) if len(nodes[node][idx]) == 4 else ''}", Class=nodes[node][idx][0].lower()), data_value=data_value)

	doc['nodes'] <= SECTION(t)

	# working on
	notes = [
		'Move select/search to a floating bar',
		'Add a summary of required and obtained ascension points'
	]
	s = SECTION(P(x) for x in notes)
	doc['todo'] <= s


init_page()
doc['loading'] <= DIV(Id='prerendered')
