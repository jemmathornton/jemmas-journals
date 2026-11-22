/* The site’s content, kept apart from the code (js/app.js draws the pages from it).
   Everything here is a PLACEHOLDER from the family template: replace it with her own words, or with an app’s own text word for word.
   Never fill it with made-up text (her rule): anything still missing stays null, and the page shows a marked placeholder.

   items: the example list (#/list) and one page each (#/item/<id>).
     id     the address (lower case, a–z, 0–9 and hyphens)
     title  the name shown
     about  her words about it, or null for a marked placeholder */
window.SITE_DATA = {
  intro: null,   // the home page’s introduction, in her own words (null shows a marked placeholder)
  listTitle: "Examples",   // the list page’s heading: a label, rename it to what the list holds
  items: [
    { id: "example-1", title: "Example 1", about: null, placeholder: true },
    { id: "example-2", title: "Example 2", about: null, placeholder: true },
    { id: "example-3", title: "Example 3", about: null, placeholder: true },
  ],
};
