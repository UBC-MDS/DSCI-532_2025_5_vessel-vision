# Milestone 4 - Finalizing your dashboard


## 1. Expectations for working collaboratively on GitHub
 For this part we created so many PR and collaborate all of our challenges there. We also created issues for each task and assign them to the group members. We also created a project board to track the progress of our tasks.

## 2. Address feedback from me and your peers

Feedbacks addressed from Professros:
- fix the table and make the line graph shorter so you won't have scrolling based on. 
- The professor advised us to "add caching to your project to optimize performance and reduce computation time, especially for expensive or repetitive tasks. 

Feedbacks adressed from our Peers
- Removed "DSCI_553" from the "About" section.
- Add a tooltip or something to indicate the country name on table.
- Data not showing up on Render.
- Add description for date filter.
- Make the dashboard title stand out with a big heading. 



## 3. Performance improvements
### Data Loading & Preprocessing:
- We loaded and preprocessed vessel data in `data.py`, combining CSV files into a single DataFrame.
- We used vectorized operations for calculating the anchored duration, significantly speeding up the process by avoiding loops.
- The data was filtered by a date parameter if provided, ensuring we only worked with relevant data.

### Caching:
- To improve app performance, we implemented caching using Flask-Caching. This allowed us to cache the processed datasets and graphs (such as the port table, trend graph, and map).

### Dashboard Layout:
- We designed the layout using Dash's components, creating a user-friendly interface. This included summary metrics, filters, and sections for displaying the map, port data, and trend graphs.

### Data Handling for Remote Deployment:
- For remote deployment, we used CSV files to avoid memory and rendering issues, since Parquet files caused memory errors due to the large data size. While Parquet files were faster for local use, we opted for CSV files in the remote environment to ensure stability and smooth performance.

## 4. App refinement
This week, we focused on tying everything together and delivering a production-ready app. We made several enhancements to improve both the functionality and the overall user experience.

1. **Date Filtering Label**: 
   - We added a label to the date filtering options to provide more clarity for users, ensuring they know exactly what data they are working with.

2. **Trend and Table Resizing**: 
   - We reduced the sizes of the trend and table sections to create more space for the map. This ensured that the map, which is a key feature of the dashboard, was given the attention it deserves.
3. **Header Addition**: 
   - A header was added to reflect the content of our dashboard. This helps users understand the purpose of the dashboard at a glance.

4. **Tooltips for Charts and Map**: 
   - We added tooltips to all the charts and map for enhanced interactivity. This provides additional context for each element and helps users better understand the data they are viewing.

By implementing these changes, we have made significant improvements to the app's usability and visual appeal, while maintaining a focus on functionality.

## 5. Smaller fixes and touch-ups

- **Tab Title**: We have updated the tab title of the dashboard in the browser to make it more descriptive and reflective of the final stage of the app.

- **GIF Animation**: The GIF animation in the README has been updated. The previous GIF has been overwritten with a new one that accurately represents the current state of the app, reflecting all recent changes and updates.

- **README**: Upon review, there was no need to make significant changes to the README file, as everything is consistent and up-to-date. The instructions are clear, and the content still accurately describes the app's functionality. As such, there were no major updates to the README.

- **Map and Toolbar**:  
    Our map covers the entire West Coast of North America. In order to focus on specific regions, users need to zoom in on the map to see the exact area they are interested in. For this reason, we decided to keep the toolbar for the map, as it includes zoom and panning options that are essential for better navigation and interaction with the map.

- **Table and Navigation**:  
    For the table, we’ve added buttons to allow users to view more port names. The "Next" button, for example, helps navigate through the data easily. This ensures the user can explore the entire data set without feeling limited by the visible portion of the table.


## 6. Reflection

In comparison to Milestone 3, our dashboard is now much faster. We implemented several techniques to improve its performance, and this speed improvement is easily noticeable in the deployed version. Some of the key optimizations we made include:

- **Vectorization**: We used vectorized operations to speed up data processing, eliminating the need for slow loops.
- **Caching**: We added caching to the dashboard, which helped improve performance by reducing the time spent on recalculating or reloading data.
- **Layout Refinements**: We refined the layout to make the dashboard more user-friendly. This includes changes such as repositioning charts and adding additional tooltips and labels for better clarity.
  
Regarding **corner cases**, we initially thought that using Parquet files would improve the dashboard's performance. However, when rendering, we encountered memory errors due to the large file size. As a result, we reverted to using CSV files, which provided better stability for the dashboard's performance, despite not being as fast as Parquet files.

In terms of changes from our initial proposal/sketch, we made several adjustments based on feedback from the professors and TAs. Notable modifications include:

- **Repositioning of charts**: We adjusted the positioning of some charts to provide more space for the map, ensuring better visibility and usability.
- **Filtering adjustments**: We updated the filtering options, especially by changing the position of the filters, to improve user experience.
- **Header update**: The header of the dashboard was updated to better reflect the content and functionality of the dashboard.
- **Date filtering removal**: Initially, we had a date filtering feature, but we decided to remove it since the dashboard is now designed to show data for just one day. Date filtering is no longer necessary for the user.
- **Card modifications**: We removed percentages from some of the cards, as they only made sense when a date filter was in place.

In terms of **visualization best practices**, we focused on improving clarity and simplicity. We made sure that the data presented is easy to interpret, and we added tooltips and labels where needed to guide the user. However, there were still some challenges, such as the memory issue with the Parquet files, which we had to work around. If we had more time, we would have further optimized the layout and added more interactivity to the visualizations.

Overall, the dashboard is in a much better place now than it was in Milestone 3. Its performance is smoother, and it is more user-friendly. Going forward, we would consider adding more features such as dynamic date selection or the ability to export data directly from the dashboard.


## 7. Set up tests and write docstrings (Optional)
- As part of refining our project and ensuring it is maintainable and easily understandable, we made sure that all of our functions have docstrings.