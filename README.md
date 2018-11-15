_This is a project for [NaNoGenMo](https://github.com/NaNoGenMo). The idea is to scrape UFO sightings and turn the reports into poems_

## Getting UFO Data
> Scrape responsibly, see https://www.scrapehero.com/how-to-prevent-getting-blacklisted-while-scraping/#easiest-way-to-find-if-a-site-doesnt-want-data-to-be-scraped

I'm using http://ufostalker.com to get the data, mainly because the reports are much more interesting than official sightings.

### Running
First run `pipenv isntall` and `pipenv shell` to start the environment.

`python main.py` will start the scraping.

### Proxies
Proxies are generated via `proxies = gen_proxies`. This will populate a text file with a list of I.P addresses to use.

### Pool
Pool is set to 10: `with Pool(10) as p:` which means 10 requests. This can be increased or decreased. But be nice and don't actually DoS a site. :heart:

## Writing the poems
Once the database is populated, run `python writer.py` this will generate a `ufo_poems.md` file. There are over 90,000 sightings so for efficiency I'm just using the latest 4000 (which will equate to > 50,000 words in total) e.g `data = get_data()[:4000]`. To get all the sightings, just remove the slice.

Example of poems: [ufo_poems.md](https://github.com/kevinhowbrook/ufo-poems/blob/master/ufo_poems.md)
