from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# for local hosting, since selenium requires a hosted page to work correctly
import http.server
import socketserver
import threading

from os import getcwd
# make it pretty
from bs4 import BeautifulSoup as bs
import minify_html
import re


# load the page in firefox-selenium and return the html
def load_page_firefox(page_name):
	from selenium.webdriver.firefox.options import Options
	profile = webdriver.FirefoxProfile()
	profile.set_preference("permissions.default.image", 2)

	options = Options()
	options.headless = True
	options.log.level = "fatal"
	driver = webdriver.Firefox(options=options, executable_path=getcwd() + '\\geckodriver.exe', firefox_profile=profile)
	driver.get(page_name)
	try:
		WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "prerendered")))
	except TimeoutException as err:
		print(err)
		exit(-1)
	html = driver.find_element_by_tag_name('html').get_attribute('outerHTML')
	driver.quit()
	return html


# make some modifications to the page
def update_page(soup):
	meta1 = soup.new_tag('meta')
	meta1['name'] = 'description'
	meta1['content'] = 'Divinity Original Sin 2 Epic Encounters Ascension Planner.'
	meta2 = soup.new_tag('meta')
	meta2['name'] = 'keywords'
	meta2['content'] = 'best videogames, free to play, free game, online games, fantasy games, PC games, PC gaming, Divinity Original Sin 2,character planner'
	soup.head.extend([meta1, meta2])
	soup.find('meta', {'name': 'robots'}).extract()
	soup.find('script', {'src': 'gen_page.py'})['src'] = 'main.py'


# add keyword titles
def keyword_title(soup):
	l_items = {
		"Abeyance": [
			 "When Abeyance activates, it instantly heals whatever damage it activated from; at the start of your next turn, suffer that amount +15% as unresistable damage, split evenly between your armors and Vitality. Any remaining damage to armor is instead dealt to Vitality.",
			"Basic activation: If it is not your turn, when you are dealt combat damage equivalent to at least 30% of your maximum Vitality (-0.5% per Inertia or Form embodied, minimum of 20%) at once, Abeyance activates."
		],
		"Adaptation": [
			"When Adaptation is activated, gain or lose up to 30% of your maximum Physical or Magic Armor until their current values equilibrate; loss occurs from the higher of the two values and restoration occurs to the lower of the two values. Additionally, gain a stacking Adaptation status, which lasts for 1 turn, stacks up to 10 and grants +2.5% to FIN, CON, POW, and WIT per stack."
			"Adaptation skill: 1 AP, no cooldown, activate Adaptation when cast."
		],
		"Benevolence": [
			"When Benevolence is activated, remove 2 stacks of Battered and Harried from the target and move half these stacks (rounded up) onto yourself. Restore 5% of your missing Vitality per stack of Battered or Harried removed this way.",
			"Gain Mercy, 2 AP, 1 turn cooldown, activate Benevolence on each ally within 8m."
		],
		"Celestial": [
			"1 AP reaction that restores 15% of target's Vitality (+2% per Life embodied).",
			"This is a Reaction: Reactions are performed automatically when their conditions are satisfied, and can only be performed when it is not the reacting character's turn."
		],
		"Centurion": [
			"1 AP reaction that performs a basic attack on a target within weapon range.",
			"This is a Reaction: Reactions are performed automatically when their conditions are satisfied, and can only be performed when it is not the reacting character's turn."
		],
		"Defiance": [
			"When you become Flanked, and when you start your turn within 5m of at least two enemies, Defiance activates for 1 turn."
		],
		"Elementalist": [
			"1 AP reaction, deals elemental damage to all characters within 2m of the reaction's target. When you perform an Elementalist reaction, suffer damage of the reaction's type, equivalent to 10% of your maximum Vitality for each stack of Elementalist you have. Then gain 1 stack of Elementalist, or 2 if using the same element twice in a row.",
			"This is a Reaction: Reactions are performed automatically when their conditions are satisfied, and can only be performed when it is not the reacting character's turn."
		],
		"Occultist": [
			"1 AP reaction, apply Bane for 2 turns. Bane deals Physical damage to the target at the beginning of their turn. When Bane ends, it deals its base damage +5% per Battered or Harried that the target suffered over its duration.",
			"This is a Reaction: Reactions are performed automatically when their conditions are satisfied, and can only be performed when it is not the reacting character's turn."
		],
		"Paucity": [
			"While active, Paucity grants +15% lifesteal (+2% per Entropy).",
			"Basic activation: Once per round, when you drop to 25% Vitality or below, activate Paucity."
		],
		"Predator": [
			"1 AP reaction that performs a basic attack on a target within weapon range. If this attack is performed with a melee weapon, it has +30% critical chance. Additionally, if this attack is performed with a dagger, attempt to sneak afterward.",
			"This is a Reaction: Reactions are performed automatically when their conditions are satisfied, and can only be performed when it is not the reacting character's turn."
		],
		"Presence": [
			"Presence is considered active on any allies that are affected by your Leadership."
		],
		"Prosperity": [
			"Basic activation: When you have at least 90% Vitality (-1% per Form or Life embodied), Prosperity is considered active."
		],
		"Purity": [
			"When Purity is activated, instantly heal 15% (+1.5% per Life embodied) of missing Vitality and armors - also gain a 10m radius aura for 2 turns that restores 8% (+1.5% per Life embodied) of missing Vitality, Magic, and Physical Armor per turn to yourself and allies. 4 turn Cooldown.",
			"Basic activation: When reduced to 30% Vitality (+1.5% per Life embodied) or below, activate Purity."
		],
		"Violent Strike": [
			"If Violent Strike is active when you use a skill, basic attack or reaction, perform a Violent Strike on the first enemy you hit, which deals 30% of your weapon damage to enemies within 2m of that target."
		],
		"Vitality Void": [
			"When Vitality Void is activated, deal piercing damage, split between all enemies within 3m of you, equal to 11% of your maximum Vitality (+1% per Entropy embodied), and you heal for 15% (+2% per Entropy embodied) of this damage. Vitality Void is not affected by increases or reductions to your damage.",
			"Basic activation: Whenever you spend a Source Point in combat, activate Vitality Void."
		],
		"Volatile Armor": [
			"Whenever you suffer damage to armor of the designated type, deal the listed percentage of that damage to all characters within range, as whatever damage type is noted."
		],
		"Voracity": [
			"Whenever an enemy dies in combat, your Voracity effects are granted to you. If the dying enemy was a summon, you are instead granted only 20% of these effects' intended values."
		],
		"Ward": [
			"When Ward is active, gain +10% to all resistances.",
			"Basic activation: After you have suffered total damage exceeding 60% of your total Vitality (-0.5% per Constitution over 10, minimum of 20%), activate Ward for 1 turn."
		],
		"Wither": [
			"Withered reduces the effect of Power by 15% (+2% per your Entropy embodied). Additionally, once per round per target, Wither applies 1 Battered and Harried as it is applied."
		]
	}
	for keyword in l_items:
		findkeyword = soup.find_all(text=re.compile(keyword))
		n_text = '\n'.join(l_items[keyword])
		p_p_p_parent = None
		for comment in findkeyword:
			c_parent = comment.parent
			if not c_parent:
				continue
			while c_parent.name not in ['table', 'section']:
				c_parent = c_parent.parent
			if not p_p_p_parent:
				p_p_p_parent = c_parent
			elif p_p_p_parent == c_parent:
				continue
			else:
				p_p_p_parent = c_parent
			fixed_text = str(comment).replace(keyword, f'<span title="{n_text}" class="keyword">{keyword}</span>', 1)
			comment.replace_with(bs(fixed_text, "html.parser"))


def main():
	# where is the server
	port = 62435
	handler = http.server.SimpleHTTPRequestHandler
	server = socketserver.TCPServer(("", port), handler)
	thread = threading.Thread(target=server.serve_forever)
	thread.daemon = True  # so the server dies when the program exits
	thread.start()
	local_page = f'http://localhost:{port}/dynamic_page.html'

	html = load_page_firefox(local_page)
	server.shutdown()  # kill the server since we are done with it
	soup = bs(html, "html.parser")
	keyword_title(soup)
	update_page(soup)
	try:
		minified = minify_html.minify(str(soup), minify_js=False, minify_css=False)
		with open('index.html', 'w', encoding='utf-8') as f:
			f.write(f"<!DOCTYPE html>{minified}")
	except SyntaxError as e:
		print(e)


if __name__ == '__main__':
	main()
