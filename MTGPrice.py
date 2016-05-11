# File name: 		MTGPrices.py 
# Autor: 			Guillermo Iglesias Birkner
# Date Created: 	09/05/2016
# Python Version: 	2.7
# Info: 			Scraper MTG Card Prices

from lxml import html
import requests
import xlsxwriter

# Open cards.txt (Edit to change input file)
read_list  = open("cards.txt","r")

# Create Excel (Edit to change output file)
workbook 	= xlsxwriter.Workbook('cards.xlsx')
worksheet 	= workbook.add_worksheet()

# Excel Format
bold 			= workbook.add_format({'bold': 1})
money_format 	= workbook.add_format({'num_format': '0.00'})

# Write first row
worksheet.write('A1', 'Card Name', bold)
worksheet.write('B1', 'Low', bold)
worksheet.write('C1', 'Medium', bold)
worksheet.write('D1', 'High', bold)

# First row
n = 2

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

	# MTG Prices TCGPlayer.com
	prices = tree.xpath('//a[@class="well-price remote-checkout"]/text()')

	# Name | Low | Mid | High 
	print card_name + ' '.join(prices[:3]) 

	if prices[:3]:
		# Write data in Excel 
		worksheet.write_string('A'+ str(n) , fixed_name1)
		worksheet.write_number('B'+ str(n) , float(prices[0].replace("$","")), money_format)
		worksheet.write_number('C'+ str(n) , float(prices[1].replace("$","")), money_format)
		worksheet.write_number('D'+ str(n) , float(prices[2].replace("$","")), money_format)
	
	else:
		# ERROR: Card has not price
		worksheet.write_string('A'+ str(n) , fixed_name1)
			
	# Count for rows
	n = n + 1

# Close cards.xlsx
workbook.close()
# Close cards.txt
read_list.close()