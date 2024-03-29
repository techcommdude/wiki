# Wiki website using Django framework and Python

This application allows users to create wiki topics/entries in Markdown format and save the entry in to the Django SQLITE3 database.  When viewing topics, Markdown content is retrieved from the database and displayed in the browser in HTML format.  The __python-markdown2__ package is used to convert the markdown to HTML and vice-versa.

This project is deployed on Heroku (have patience since the instance is likely sleeping): <a href="https://wiki-markdown-gfarnell.herokuapp.com/">https://wiki-markdown-gfarnell.herokuapp.com/</a>

A screencast of the project is available on YouTube:

<a href="http://www.youtube.com/watch?feature=player_embedded&v=XYzJSfeYuJI
" target="_blank"><img src="encyclopedia/static/encyclopedia/wiki.gif"
alt="Wiki by Geoff Farnell" width="600" height="360" /></a>

Some of the technologies I used when building the wiki app:

* Visual Studio Code
* Django web framework
* Python
* Git
* HTML
* CSS

-----------
## Project overview

* **Entry Page**: Visiting */wiki/TITLE*, where **TITLE** is the title of an encyclopedia entry, will render a page that displays the contents of that encyclopedia entry.
    * The view gets the contents of the encyclopedia entry by calling the appropriate utility function.
    * If an entry is requested that does not exist, the user is presented with an error page indicating that their requested page was not found.
    * If the entry does exist, the user is presented with a page that displays the content of the entry. The title of the page includes the name of the entry.

* **Index Page**: The *index.html* lists the names of all pages in the encyclopedia and the user can click on any entry name to be taken directly to that entry page.

* **Search**: The user can type a query into the search box in the sidebar to search for an encyclopedia entry.
    * If the query matches the name of an encyclopedia entry, the user is redirected to that entry’s page.
    * If the query does not match the name of an encyclopedia entry, the user is instead be taken to a search results page that displays a list of all encyclopedia entries that have the query as a substring. For example, if the search query were *ytho*, then Python should appear in the search results.
    * Clicking on any of the entry names on the search results page takes the user to that entry’s page.

* **New Page**: Clicking “Create New Page” in the sidebar takes the user to a page where they can create a new encyclopedia entry.
    * Users can enter a title for the page and, in a textarea, can enter the Markdown content for the page.
    * Users can click a button to save their new page.
    * When the page is saved, if an encyclopedia entry already exists with the provided title, the user is presented with an error message.
    Otherwise, the encyclopedia entry is saved to disk, and the user is taken to the new entry’s page.

* **Edit Page**: On each entry page, the user can click a link to be taken to a page where the user can edit that entry’s Markdown content in a textarea.
    * The textarea is pre-populated with the existing Markdown content of the page. (i.e., the existing is the initial value of the textarea).
    * The user can click a button to save the changes made to the entry.
    * Once the entry is saved, the user is redirected back to that entry’s page.

* **Random Page**: Clicking “Random Page” in the sidebar takes the user to a random encyclopedia entry displayed in HTML format that the user can then edit.

* **Markdown to HTML Conversion**: On each entry’s page, any Markdown content in the entry file is converted to HTML before being displayed to the user. The python-markdown2 package is used to perform this conversion.

## Screen captures of the application
### Home page:
![Wiki project](Wiki_page.png)
### Markdown editing for an entry:
![Markdown editing](Wiki_page2.png)
### HTML display for an entry:
![HTML display](Wiki_page3.png)
