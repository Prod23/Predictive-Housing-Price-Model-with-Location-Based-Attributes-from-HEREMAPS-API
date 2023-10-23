# Predictive-Housing-Price-Model-with-Location-Based-Attributes-from-HEREMAPS-API

### Goal: To predict the Real Estate Prices in Bengaluru, India based on Location-based attributes
### Approach: After researching various property broker sites and talking to experts involved in the real estate industry, we came up with a list of factors on which the price of a property depends:
-Location
*Sq. Ft
*BHK
*No. of Hospitals Nearby
*No. of Parks Nearby
*No. of Schools Nearby
*No. of houses nearby(to determine whether it is a residential area or not)
*No. of Stores Nearby
*No. of Malls Nearby
*No. of Metro Stations Nearby
*No. of restaurants nearby

### Method:
Step 1: Scraped the data from Magicbricks website, and saved it in 'household.csv' file
Step 2: Performed EDA on the dataframe
Step 3: Using Geocode API from HERE Maps, we found out the (latitude,longitude) values for each location
Step 4: Using BrowseSearch API from HERE Maps, we found out the different proxies for development 
