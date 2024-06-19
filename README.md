# Shelf Help 
![Shelf Help](frontend/public/images/ios/144.png) 

<a href="https://www.buymeacoffee.com/michaelchapman" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-yellow.png" alt="Buy Me A Coffee" height="41" width="174"></a>

Do you have a really large `to-read` shelf on Goodreads, and need some help deciding what to read next?

Do you also love the library, whether it be physical books or using [Libby](https://libbyapp.com/)?

If you answered yes to either of those questions, then [Shelf Help](https://shelfhelp.onrender.com) is a great app for you!


## Background
The idea for this came about when I was browsing my Goodreads app while in the library trying to pick out what to read next.
I was frustrated that I couldn't randomly sort in the app because things I recently put on there were at the top by default,
but even then, I didn't have a way to know if it was available at my library.

I decided to put together a quick prototype project, originally in [Plotly's Dash](https://dash.plotly.com/) framework.
Professionally, I had built Dash apps before, but I recently discovered how you can host these webapps on [Render](https://render.com/), and it made me want to make something I could share more broadly.

So I figured I'd take a dive into React and make a bit more modern app, with a better look and feel, and here we are!

## Contributing
If there is anything you'd like to see done here, throw up an issue here on Github!

Or if you want to help contribute directly, put up an issue and a branch.

**BEFORE YOU PUT UP A PR** please make sure you put one of these 4 terms in the title so that Render doesn't build the preview environment yet:
* `[skip render]`
* `[skip preview]`
* `[render skip]`
* `[preview skip]`

I am currently hosting everything right now, and currently on the free plan. If it gets more usage, then I'll investigate spending more to improve performance for more users.

If you feel so inclined and would like to support monetarily, feel free to use the "Buy me a coffee" link above!

## Requirements:
### Back End
* Python `3.12.3`
* See `/backend/requirements.txt`
### Front End
* [Yarn](https://yarnpkg.com/getting-started/install)
* [Vite](https://vitejs.dev/guide/)
* See `/frontend`
