from browser import document as doc
from browser.html import TABLE, TR, TH, TD, INPUT, SELECT, SECTION, DIV, OPTION, BR, COL, H1, BUTTON
from json import load
from collections import defaultdict


def init_page():
	# set up page search functions
	always_show = SELECT(Id=f"always_show", Class=f"save onehundred")
	for s in ['no', 'yes']:
		always_show <= OPTION(s.capitalize(), value=s)

	t = TABLE(TR(TH() + TH('Selection')))
	t <= TR(TD("Only Show Selected Ascendancies:", Class="right_text") + TD(always_show))
	t <= TR(TD("Keyword(s) Search:", Class="right_text") + TD(INPUT(Type='text', Id="keywords", Class='save') + BUTTON('x', Id='clear_keywords')))
	doc['filter'] <= t

	# set up ascendancies
	with open('node_data.json', 'r') as f:
		data = load(f)
	nodes = defaultdict(list)
	for domain in data:
		s = SECTION(H1(domain), Class=domain.lower())
		for item in data[domain]:
			data_value = ', '.join([z for x in item['nodes'] for y in x for z in y] + [y for x in item['implicit'] for y in x if y]).lower()
			t = TABLE(COL(Class='first_column') + COL() + COL(), Class='onehundred borders', data_value=data_value)
			t <= TR(TH(INPUT(type='checkbox')) + TH(item['name']) + TH(f"Tier {item['tier']}"))
			req = ', '.join([f"{item['require'][x]} {x}" for x in item['require']])
			comp = ', '.join([f"{item['complete'][x]} {x}" for x in item['complete']]) if 'complete' in item else 'Nothing'
			t <= TR(TH() + TH(f"Required: {req}") + TH(f"Completion: {comp}"))
			t <= TR(TH('Selection') + TH('Value(s)') + TH('Implicit(s)'))
			for c in range(len(item['nodes'])):
				rspan = len(item['nodes'][c])
				cell_vals = ', '.join([y for x in item['nodes'][c] for y in x] + [x for x in item['implicit'][c] if x]).lower()
				n = ', '.join(item['nodes'][c][0])
				nodes[n].append((domain, item['name'], c, 0))
				t <= TR(TD(f"{c}: " + SELECT(OPTION(x, value=f"{x}") for x in ['Any'] + list(range(rspan))), rowspan=rspan) + TD(n) + TD(', '.join(item['implicit'][c]), rowspan=rspan), data_value=cell_vals)
				for idx in range(1, len(item['nodes'][c])):
					n = ', '.join(item['nodes'][c][idx])
					nodes[n].append((domain, item['name'], c, idx))
					t <= TR(TD(n), data_value=cell_vals)
			t <= TR(TH(item['flavor'], colspan=3))
			s <= t
		doc['ascensions'] <= s

	# set up nodes list
	t = TABLE(TR(TH("Node") + TH('Location(s)')), Class='onehundred borders')
	for node in sorted(nodes):
		t <= TR(TD(node, rowspan=len(nodes[node])) + TD(str(nodes[node][0]), Class=nodes[node][0][0].lower()), data_value=node.lower())
		for idx in range(1, len(nodes[node])):
			t <= TR(TD(str(nodes[node][idx]), Class=nodes[node][idx][0].lower()), data_value=node.lower())

	doc['nodes'] <= t


init_page()
doc['loading'] <= DIV(Id='prerendered')
