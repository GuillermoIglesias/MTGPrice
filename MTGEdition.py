# File name: 		MTGEdition.py 
# Autor: 			Guillermo Iglesias Birkner
# Date Created: 	21/05/2016
# Python Version: 	2.7
# Info: 			Scraper MTG Card Edition

from lxml import html
import requests
import xlsxwriter

# Open cards.txt (Edit to change input file)
read_list  = open("cards.txt","r")

# Create Excel (Edit to change output file)
workbook 	= xlsxwriter.Workbook('cards.xlsx')
worksheet 	= workbook.add_worksheet()

# Initial Row
row = 0

# Reading each line
for line in read_list:
	
	# Card name
	card_name = line

	# Fixed card name 
	fixed_name1 = card_name.replace("\n","")
	fixed_name2 = fixed_name1.replace("'","")
	fixed_name3 = fixed_name2.replace(",","")
	fixed_name4 = fixed_name3.replace("  flip","")
	fixed_name5 = fixed_name4.replace("  Flip","")
	fixed_name6 = fixed_name5.replace(" ","-")
	fixed_name7 = fixed_name6.replace("/","-")

	# URL Tappedout.net default
	URL = "http://tappedout.net/mtg-card/"

	# HTML storage
	page = requests.get(URL+fixed_name7)
	tree = html.fromstring(page.content)

	# MTG Editions TCGPlayer.com
	editions = tree.xpath('//a[contains(@href,"/mtg-set/")]/text()')

	# Name | Editions
	print card_name
	print editions	

	if editions:
		# Write data in Excel 
		worksheet.write_string(row, 0, fixed_name1)
		col = 1 
		for i in editions:
			worksheet.write_string(row, col, i)
			col = col + 1
	
	else:
		# ERROR: Card has not edition
		worksheet.write_string(row, 0, fixed_name1)

	# Move Row	
	row = row + 1
			
# Close cards.xlsx
workbook.close()
# Close cards.txt
read_list.close()