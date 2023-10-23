# Predictive-Housing-Price-Model-with-Location-Based-Attributes-from-HEREMAPS-API

## Goal: 
To predict the Real Estate Prices in Bengaluru, India based on Location-based attributes
## Approach: 
After researching various property broker sites and talking to experts involved in the real estate industry, we came up with a list of factors on which the price of a property depends:
- Location
- Sq. Ft
- BHK
- No. of Hospitals Nearby
- No. of Parks Nearby
- No. of Schools Nearby
- No. of houses nearby(to determine whether it is a residential area or not)
- No. of Stores Nearby
- No. of Malls Nearby
- No. of Metro Stations Nearby
- No. Of restaurants nearby
## Tech Stack and APIs used
### Backend: 
- Google Colab, Python, ScikitLearn, Pandas, Matplotlib, HERE Search - Forward Geocoder API, HERE Search - Browse API, HERE Maps API,HERE Autosuggest API.
### Frontend:
- HTML, CSS, Javascript


## Model Significance:
- When a person wants to buy a house, they want to look for the availability of hospitals for the wellbeing of their parents/old people and schools for their children.
- A number of restaurants, malls and metro stations in an area means it is a developing area with many commercial spots. 
- As a proxy for future development, we assume places close to maps and restaurants will see greater economic growth and use these parameters to predict prices.
- We define a radius for different parameters.
- For example, a person would need a hospital or school closer to their house than a restaurant. 



## Method:
- Step 1: Scraped the data from Magicbricks website, and saved it in 'household.csv' file
- Step 2: Performed EDA on the dataframe
- Step 3: Using HERE Search - Forward Geocode API from HERE Maps, we found out the (latitude,longitude) coordinate values from text values of each location.
- Step 4: Using HERE Search - Browse API from HERE Maps, we found the different proxies for development like Hospitals, Parks etc. We used different radius for each attribute, like a hospital should be closer to a house than a restaurant, for example. Using this, we will be taking the count for each location.
- Step 5: We then performed a Linear Regression on the data, 

