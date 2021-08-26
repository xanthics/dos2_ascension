from browser import document as doc
from browser import bind, window
from browser.html import TABLE, TR, TH, TD, INPUT, SELECT, OPTION, DIV, BUTTON, SPAN, LI, H2, H3, IMG, COLGROUP, COL, SECTION
from browser.local_storage import storage


def load_page():
	# add navigation buttons
	pages = ['ascensions', 'nodes', 'todo']  # , 'About', 'Changelog']
	for c, page in enumerate(pages):
		doc['nav_buttons'] <= BUTTON(page.capitalize(), data_id=page, Class=f'page{" current_tab" if not c else ""}', Id=f'b_{page}')

	doc["clear_keywords"].bind("click", clear_keywords)

	# Make it so navigation buttons work
	@bind('.page', 'click')
	def change_page(ev):
		l_val = ev.target['data-id']
		doc[l_val].style.display = 'block'
		doc[f'b_{l_val}'].attrs['class'] = 'current_tab page'
		idx = pages.index(l_val)
		for i in pages[:idx] + pages[idx+1:]:
			doc[i].style.display = 'none'
			doc[f'b_{i}'].attrs['class'] = 'page'


# Function handling filtering changes
@bind('.save', 'input')
def save_state(ev):
	if ((ev.target.id in ['always_show'] or ev.target.type == 'checkbox') and not doc['keywords'].value) or (ev.target.id == 'keywords' and not ev.target.value):
		init_page()
	elif ev.target.id == 'keywords':
		search_terms = ev.target.value.lower().split()
		for el in doc.get(selector="[data-value]"):
			terms = el.attrs['data-value']
			if all(x in terms for x in search_terms):
				if 'hidden_class' in el.class_name:
					el.attrs['class'] = "container"
				elif 'hidden' in el.attrs:
					del el.attrs['hidden']
			else:
				if 'container' in el.class_name:
					el.attrs['class'] = "container hidden_class"
				else:
					el.attrs['hidden'] = ''


# Clear keyword box
def clear_keywords(ev):
	doc['keywords'].value = ''
	event = window.Event.new('input')
	doc['keywords'].dispatchEvent(event)


# Set the page visibility state
def init_page():
	# Only update visibility if keywords is empty
	if not doc['keywords'].value:
		always_show = True if doc['always_show'].value == 'no' else False
		for el in doc.get(selector="[data-value]"):
			if always_show and 'container' not in el.class_name:
				if 'hidden_class' in el.class_name:
					el.attrs['class'] = "container"
				elif 'hidden' in el.attrs:
					del el.attrs['hidden']
			else:
				if 'container' in el.class_name:
					el.attrs['class'] = "container hidden_class"
				else:
					el.attrs['hidden'] = ''


load_page()
init_page()
del doc['loading']
