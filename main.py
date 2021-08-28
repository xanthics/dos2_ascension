from browser import document as doc
from browser import bind, window
from browser.html import TABLE, TR, TH, TD, INPUT, SELECT, OPTION, BUTTON, SPAN, LI, H2, H3, IMG, COLGROUP, COL, SECTION
from resource_vals import asc, nodes


def load_page():
	# add navigation buttons
	pages = ['ascensions', 'nodes', 'todo']  # , 'About', 'Changelog']
	for c, page in enumerate(pages):
		doc['nav_buttons'] <= BUTTON(page.capitalize(), data_id=page, Class=f'page{" current_tab" if not c else ""}', Id=f'b_{page}')

	doc["clear_keywords"].bind("click", clear_keywords)

	# if there is a query string try to load it
	if any(x in doc.query for x in ['asc', 'nodes']):
		doc['always_show'].value = 'yes'
		if 'asc' in doc.query:
			for asc in doc.query['asc'].split(','):
				doc[asc].checked = True
		if 'nodes' in doc.query:
			for node in doc.query['nodes'].split(','):
				doc[node[:-1]].value = node[-1]

	gen_have_need()

	# Make it so navigation buttons work
	@bind('.page', 'click')
	def change_page(ev):
		l_val = ev.target['data-id']
		doc[l_val].style.display = 'block'
		doc[f'b_{l_val}'].class_name = 'current_tab page'
		idx = pages.index(l_val)
		for i in pages[:idx] + pages[idx+1:]:
			doc[i].style.display = 'none'
			doc[f'b_{i}'].class_name = 'page'


# update have and need
def gen_have_need(t_asc=None, t_nodes=None):
	if not t_asc:
		t_asc = [el.id for el in doc.get(selector=":checked") if el.id]
	if not t_nodes:
		t_nodes = [f"{el.id}{el.value}" for el in doc.get(selector="select.save") if el.value != 'Any']
	have = {'Force': 0, 'Life': 0, 'Form': 0, 'Inertia': 0, 'Entropy': 0}
	need = {'Force': 0, 'Life': 0, 'Form': 0, 'Inertia': 0, 'Entropy': 0}
	for n in t_nodes:
		if n in nodes and f'c-{n}' in t_asc:
			have = {x: have[x] + nodes[n].get(x, 0) for x in have}
	for n in t_asc:
		if n in asc:
			have = {x: have[x] + asc[n]['complete'].get(x, 0) for x in have}
			need = {x: max(need[x], asc[n]['require'].get(x, 0)) for x in need}
	missing = {x: (need[x] - have[x] if need[x] - have[x] > 0 else '') for x in have}

	t = TABLE(TR(TD() + TD('Force', Class='force') + TD('Life', Class='life') + TD('Form', Class='form') + TD('Inertia', Class='inertia') + TD('Entropy', Class='entropy')), Class='onehundred borders')
	t <= TR(TD('Required') + TD(need['Force']) + TD(need['Life']) + TD(need['Form']) + TD(need['Inertia']) + TD(need['Entropy']))
	t <= TR(TD('Have') + TD(have['Force']) + TD(have['Life']) + TD(have['Form']) + TD(have['Inertia']) + TD(have['Entropy']))
	t <= TR(TD('Missing') + TD(missing['Force'], Class='force' if missing['Force'] else '') +
							TD(missing['Life'], Class='life' if missing['Life'] else '') +
							TD(missing['Form'], Class='form' if missing['Form'] else '') +
							TD(missing['Inertia'], Class='inertia' if missing['Inertia'] else '') +
							TD(missing['Entropy'], Class='entropy' if missing['Entropy'] else ''))

	doc['have_need'].text = ''
	doc['have_need'] <= t


# Function handling filtering changes
@bind('.save', 'input')
def save_state(ev):
	update_page(ev.target.id, ev.target.type)
	# calculate required and generated ascendancy resources
	t_asc = [el.id for el in doc.get(selector=":checked") if el.id]
	t_nodes = [f"{el.id}{el.value}" for el in doc.get(selector="select.save") if el.value != 'Any']
	gen_have_need(t_asc, t_nodes)
	# update query string
	calc_asc = ','.join(t_asc)
	calc_asc = 'asc=' + calc_asc if calc_asc else ''
	calc_node = ','.join(t_nodes)
	calc_node = 'nodes=' + calc_node if calc_node else ''
	window.history.replaceState('', '', f"?{calc_asc}{'&' if calc_asc and calc_node else ''}{calc_node}")


# Function handling filtering changes
@bind('.filter', 'input')
def update_state(ev):
	if ev.target.id == 'keywords' and doc['keywords'].value:
		search_terms = ev.target.value.lower().split()
		for el in doc.get(selector="[data-value]"):
			terms = el.attrs['data-value']
			if all(x in terms for x in search_terms):
				if 'hidden' in el.attrs:
					del el.attrs['hidden']
			else:
				el.attrs['hidden'] = ''
		for el in doc.get(selector="[data-content]"):
			terms = el.attrs['data-content']
			if all(x in terms for x in search_terms):
				if 'hidden_class' in el.class_name:
					el.class_name = el.class_name.replace('hidden_class', '').strip()
			else:
				el.class_name += ' hidden_class'
	else:
		update_page()


# Clear keyword box
def clear_keywords(ev):
	doc['keywords'].value = ''
	event = window.Event.new('input')
	doc['keywords'].dispatchEvent(event)
	update_page()


# Set the page visibility state
def update_page(tar_id=None, tar_type=None):
	always_show = True if doc['always_show'].value == 'no' else False
	if tar_type == 'select-one':
		el_idx = -1 if doc[tar_id].value == 'Any' else int(doc[tar_id].value)
		for idx in range(1, len(doc[tar_id].options)):
			if el_idx < 0 or idx == el_idx:
				doc[doc[tar_id].id + str(idx)].class_name = doc[doc[tar_id].id + str(idx)].class_name.replace('demphasis', '').strip()
			else:
				doc[doc[tar_id].id + str(idx)].class_name += ' demphasis'
	else:
		# Only update visibility if keywords is empty
		if not doc['keywords'].value:
			# show all hidden table data
			for el in doc.get(selector=".hidden_class"):
				el.class_name = el.class_name.replace('hidden_class', '').strip()
			# change cell emphasis based on dropdown selection
			for el in doc.get(selector="select.save"):
				el_idx = -1 if el.value == 'Any' else int(el.value)
				for idx in range(1, len(el.options)):
					if el_idx < 0 or idx == el_idx:
						doc[el.id + str(idx)].class_name = doc[el.id + str(idx)].class_name.replace('demphasis', '').strip()
					else:
						doc[el.id + str(idx)].class_name += ' demphasis'
			for el in doc.get(selector="[data-asc-id]"):
				if always_show or doc[f'c-{el.attrs["data-asc-id"]}'].checked:
					if 'hidden' in el.attrs:
						del el.attrs['hidden']
				else:
					el.attrs['hidden'] = ''


load_page()
update_page()
del doc['loading']
