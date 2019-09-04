import json
import pandas
import argparse
from linkedin import Linkedin

def json_to_csv(filename):
	count = 0
	content = []
	batches = json.load(open(filename,'r'))
	for batch in batches:
		if "included" in batch:
			for element in batch['included']:
				if "$type" in element and element["$type"] == "com.linkedin.voyager.feed.Update":
					if "content" in element["value"] and "title" in element["value"]["content"]:
						text = ""
						if "text" in element["value"]["content"] and "values" in element["value"]["content"]["text"]:
							for value in element["value"]["content"]["text"]["values"]:
								text += value["value"]
							article = {
								"title": element["value"]["content"]["title"],
								"text": text
							}
							content.append(article)
							count += 1
	df = pandas.DataFrame(content)
	df.to_csv(filename + '.csv')

parser = argparse.ArgumentParser(description='This script extract reviews from the Linkedin public feed.')
parser.add_argument('-k', '--keywords', default='technology', help="The words to search.")
parser.add_argument('-u', '--user', default='', help="Linkedin email.")
parser.add_argument('-p', '--password', default='', help="Linkedin password.")
parser.add_argument('-n', '--number', default=100, type=int, help="Number of results.")
parser.add_argument('-o', '--output', default='results.json', help="Output filename.")
args = parser.parse_args()

if args.user and args.password:
	api = Linkedin(args.user, args.password)
	max_results = args.number
	content = api.search_content({
		'keywords': args.keywords,
		'filters': 'List(resultType->CONTENT)',
	    'origin': 'GLOBAL_SEARCH_HEADER',
	    'queryContext': 'List()'
	}, args.number)
	json.dump(content, open(args.output, 'w'))
	json_to_csv(args.output)
else:
	print('You must provide your Linkedin credentials. Use --help for listing the options.')
