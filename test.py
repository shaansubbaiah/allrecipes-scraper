from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotVisibleException as NotVisible

import time
import pandas as pd
import re
import os

## ------------ Global variables ----------------------- ##
loc = './chromedriver' #location of Chrome webdriver
major_cats = {'Dish Type', 'World Cuisine', 'Cooking Style'} # names of Allrecipes.com major categories (section headers) to scrape
num_per_category = 100 #the number of recipes to retrieve from each subcategory
cleanup = False #whether to delete intermediate files or not once process finishes


## ------------ 
def initialize_driver():
	#start Selenium webdriver
	if loc=='':
		print('Error, please enter webdriver address. Stopping.')
		return
	
	options = Options()
	options.add_argument('--headless')
	options.add_argument('--log-level=3')

	return webdriver.Chrome(loc, options=options)
	
def main():
	# double-check that process needs to run at all
	if os.path.isfile("./scraped_data.csv"):
		print("Data has already been scraped. Check scraped_data.csv.")
		return
	
	# initialize driver
	driver = initialize_driver()
	
	# check if categories have been scraped and scrape if necessary
	if not os.path.isfile('./categories.csv'):
		print("\n----- Building category file now. -----\n")
		build_category_file(driver)
		
	# if the file of individual recipe links doesn't exist, create it
	if not os.path.isfile('./data_during_scraping.csv'):
		print("\n------- Finding individual recipe links for each category now. -----\n")
		get_links(driver, pd.read_csv("categories.csv", index_col=0))
		
	print("\n----- Scraping individual recipe links now. -----\n")
	# now the individual recipe links file exists, scrape each one until all are completed
	data = pd.read_csv("data_during_scraping.csv", index_col=0)
	data.loc[data['title'].isnull(), 'title'] = ''
	
	try:
		while len(data[data['title']==''])>0: #while there's data left to scrape
			try:
				for idx, row in data[data['title']==''].iterrows():
					data.loc[idx] = scrape_recipe_link(row, driver) #update data incrementally
					
					if idx%200==0:
						print("Completed scraping {} of {} total recipe links. {}% complete.".format(idx, len(data), round(idx/len(data)*100),2))
			except: #probably hit a time-out error from Selenium, so restart webdriver and continue
				driver.quit()
				driver = initialize_driver()
	except: #hit a more grievous, secondary error so save data and exit main function
		print("Something grievously wrong happened. Data is saving, and then program will exit.")
		data.to_csv("data_during_scraping.csv")
		return
	
	# now loop finished, data is finished being scraped
	data.to_csv("scraped_data.csv")
	
	# cleanup
	if cleanup:
		if os.path.isfile('./categories.csv'):
			os.remove("categories.csv")
		if os.path.isfile('./data_before_scraping.csv'):
			os.remove("data_before_scraping.csv")
		if os.path.isfile('./data_during_scraping.csv'):
			os.remove("data_during_scraping.csv")
	return


def build_category_file(driver):
    # go to Allrecipes.com
    driver.get('https://www.allrecipes.com/recipes/')
    
    # initialize df to hold category information
    cat_df = pd.DataFrame(columns=['cat', 'subcat', 'link'])

    # iterate over sections
    for section in driver.find_elements_by_xpath("//div[@class='all-categories-col']//section"):
        section_name = section.find_elements_by_xpath(".//h3[@class='heading__h3']")[0].text
        # skip some categories
        if section_name not in major_cats:
            continue
        # retain the subcategory name and link for the remaining categories 
        cat_df = pd.concat([cat_df, 
                        pd.DataFrame([(section_name, a.text,a.get_attribute('href')) for a in section.find_elements_by_xpath(".//ul//li//a")], columns=['cat', 'subcat', 'link'])])
    cat_df.to_csv("categories.csv")
    return
    
def get_links(driver, cat_df):		
    # either read previous version or start over
    try:
        data = pd.read_csv("data_before_scraping.csv", index_col=0)
    except:
        data = pd.DataFrame(columns=['link']+cat_df['subcat'].values.tolist())
        
    # add as much to data as possible, save file version if there's an error
    try:
        # iterate through category pages to find recipe links for each category
        for index, (subcat, link) in cat_df[['subcat', 'link']].iterrows():
            # skip if category has already been covered
            if data[subcat].sum()>0:
                continue

            # otherwise, go to category page and scrape links
            driver.get(link)

            # keep scrolling down until enough links appear
            links = driver.find_elements_by_xpath("//article//div//h3[@class='fixed-recipe-card__h3']//a")
            last_size = len(links)
            while last_size<num_per_category:
                # check if "more results" button has appeared and click if necessary
                try:
                    driver.find_element_by_id("btnMoreResults").click()
                except NotVisible:
                    pass

                # scroll window down and wait for it to load
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                links = driver.find_elements_by_xpath("//article//div//h3[@class='fixed-recipe-card__h3']//a")

                # exit if scrolling down doesn't load more links (infinite scroll error in webpage)
                if len(links)==last_size:
                    break
                last_size = len(links)
            print("Finished scraping '{}' category with {} recipe links.".format(subcat, last_size))

            # add data to dataframe
            new_data = pd.DataFrame([[card.get_attribute('href') for card in links]], index=['link']).T.reindex(columns=data.columns, fill_value=0)
            new_data[subcat] = 1
            data = pd.concat([data, new_data])
        
        # all data has been scraped
        ## remove internalSource extras in string links
        data['link'] = data['link'].apply(lambda x:x.split("?internalSource")[0])
        ## groupby link and aggregate multiple rows of the same link into a single row
        data = data.groupby('link').sum().reset_index()
        ## reindex to add columns for each recipe
        data_to_scrape = ['title', 'ratings', 'madeit', 'reviews', 'photos', 'submitter_description',
                     'ingredients', 'readyin', 'servings', 'calories', 'fat', 'carbohydrate', 'protein']
        data = data.reindex(columns=data.columns.tolist()+data_to_scrape)

        # successfully finished so save new file
        data.to_csv("data_during_scraping.csv")
    except:
        # hit error so save temporary file
        data.to_csv("data_before_scraping.csv")
        
    return

def scrape_recipe_link(s, driver):
    # if row has been updated before, don't scrape again
    if len(s['title'])!=0:
        return s
    
    #navigate to recipe
    driver.get(s['link'])
    #scrape
    try:
        s.loc['title'] = driver.find_elements_by_xpath("//h1[@class='recipe-summary__h1']")[0].text
    except:
        pass
    try:
        s.loc['ratings'] = driver.find_elements_by_xpath("//div[@class='rating-stars']")[0].get_attribute('data-ratingstars')
    except:
        pass
    try:
        s.loc['madeit'] = driver.find_elements_by_xpath("//span[@class='made-it-count ng-binding']")[0].text
    except:
        pass
    try:
        s.loc['reviews'] = driver.find_elements_by_xpath("//span[@class='review-count']")[0].text.split()[0]
    except:
        pass
    try:
        s.loc['photos'] = driver.find_elements_by_xpath("//span[@class='picture-count-link']")[0].text.split()[0]
    except:
        pass
    try:
        s.loc['submitter_description'] = driver.find_elements_by_xpath("//div[@class='submitter__description']")[0].text
    except:
        pass
    try:
        s.loc['ingredients'] = [element.text for element in driver.find_elements_by_xpath("//span[@class='recipe-ingred_txt added']")]
    except:
        pass
    try:
        s.loc['readyin'] = driver.find_elements_by_xpath("//span[@class='ready-in-time']")[0].text
    except:
        pass
    try:
        s.loc['servings'] = driver.find_elements_by_xpath("//span[@class='servings-count']//span")[0].text
    except:
        pass
    try:
        s.loc['calories'] = driver.find_elements_by_xpath("//span[@class='calorie-count']//span")[0].text
    except:
        pass
    for string in ['fatContent', 'carbohydrateContent', 'proteinContent']:
        try:
            s.loc[re.split(r"[A-Z]", string)[0]] = driver.find_elements_by_xpath("//span[@itemprop='{}']".format(string))[0].text
        except:
            pass
    return s

main()
