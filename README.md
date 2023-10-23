# Predictive-Housing-Price-Model-with-Location-Based-Attributes-from-HEREMAPS-API

## Goal: 
To predict the Real Estate Prices in Bengaluru, India based on Location-based attributes, in a 24 Hour Hackathon
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
- Step 5: We then used various models to check for accuracy. We used Linear Regression, KNN Regression, Support Vector Regression, Random Forest Regression and Gradient Boost Regression. In the end, we found maximum accuracy of 70% in Linear Regression. The reason for such a low accuracy is due to shortage of data, as we worked with limited data of 138 datapoints. Due to time constraints of the hackathon, we were encouraged by the HERE Maps team to work on full-fledged implementation of the project.
- Step 6: Created a Javascript-based web application, which used HERE Maps API to interactively display a pin on the map based on the input location address. In the backend, the coordinates are found out for the input location, and based on the other desired inputs from the user for number of bedrooms, bathrooms and Sq. Ft. data, we run a regression along with the other development attributes. We then give the latitude, longitude values and our prediction of the prices.

## Web-app images:

![WhatsApp Image 2023-10-23 at 16 35 59_88c71a5d](https://github.com/Prod23/Predictive-Housing-Price-Model-with-Location-Based-Attributes-from-HEREMAPS-API/assets/86822712/a17e93b3-c9a7-4d3e-bd63-f232a000c981)

![WhatsApp Image 2023-10-23 at 16 36 00_68d5d153](https://github.com/Prod23/Predictive-Housing-Price-Model-with-Location-Based-Attributes-from-HEREMAPS-API/assets/86822712/6ab6b604-e8dc-4609-af82-b45dadd3cd8c)

## Future Scope:
- Integrating financial variables such as prevailing interest rates, inflation, employment data to predict whether the pricing is fair or not
- Using Time Series prediction models of house prices to predict whether the investment in the real-estate property is worth it or not

