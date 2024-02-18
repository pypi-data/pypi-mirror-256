# letterboxdpy

[![PyPI version](https://badge.fury.io/py/letterboxdpy.svg)](https://badge.fury.io/py/letterboxdpy)
[![Downloads](https://static.pepy.tech/personalized-badge/letterboxdpy?period=total&units=none&left_color=grey&right_color=blue&left_text=Downloads)](https://pepy.tech/project/letterboxdpy)
![format](https://img.shields.io/pypi/format/letterboxdpy)

## Installation

```
pip install letterboxdpy
```

# Directory
 - [User Objects](#User)
    - [user_genre_info](#user_genre_info)
    - [user_following & user_followers](#user_following)
    - [user_films](#user_films)
    - [user_reviews](#user_reviews)
    - [user_diary](#user_diary)
    - [user_wrapped](#user_wrapped)
    - [user_activity](#user_activity)
    - [user_lists](#user_lists)
    - [user_watchlist](#user_watchlist)
    - [user_tags](#user_tags)
 - [Members](#Members) (todo)
    - [top_users](#top_users) (todo)
 - [Movie Objects](#Movie)
    - [movie_details](#movie_details)
    - [movie_watchers](#movie_watchers) (todo)
 - [List Objects](#List)
    - [list_tags](#list_tags)

<h1 id="User">User Objects</h1>

```python
from letterboxdpy import user
user_instance = user.User("nmcassa")
print(user_instance)
```

<details>
  <summary>Click to expand <code>User</code> object response</summary>
  
```json
{
  "username": "nmcassa",
  "id": "1500306",
  "display_name": "nmcassa",
  "bio": null,
  "location": null,
  "website": null,
  "watchlist_length": 58,
  "stats": {
    "films": 536,
    "this_year": 17,
    "list": 1,
    "following": 9,
    "followers": 7
  },
  "favorites": [
    [
      "The Grand Budapest Hotel",
      "the-grand-budapest-hotel"
    ],
    ...
  ],
  "avatar": {
    "exists": true,
    "size": [
      1000,
      1000
    ],
    "url": "https://a.ltrbxd.com/resized/avatar/upload/1/5/0/0/3/0/6/shard/avtr-0-1000-0-1000-crop.jpg"
  },
  "recent": {
    "watchlist": {
      "51707": {
        "name": "Raising Arizona",
        "slug": "raising-arizona"
      },
      ...
    },
    "diary": {
      "months": {
        "2": [
          [
            "9",
            "Argylle"
          ],
          ...
        ],
        "1": [
          [
            "29",
            "PlayTime"
          ],
          ...
        ]
      }
    }
  }
}
```
</details>

<h2 id="user_genre_info">user_genre_info(user object)</h2>

```python
from letterboxdpy import user
user_instance = user.User("nmcassa")
print(user.user_genre_info(user_instance))
```

<details>
  <summary>Click to expand <code>user_genre_info</code> method response</summary>

```json
{
    "action":55,
    "adventure":101,
    "animation":95,
    "comedy":188,
    "crime":22,
    "documentary":16,
    "drama":94,
    "family":109,
    "fantasy":54,
    "history":5,
    "horror":27,
    "music":9,
    "mystery":30,
    "romance":29,
    "science-fiction":48,
    "thriller":43,
    "tv-movie":13,
    "war":4,
    "western":5
}
```
</details>

<h2 id="user_following">user_following(user object) / user_followers(user object)</h2>

```python
from letterboxdpy import user
user_instance = user.User("nmcassa")
print(user.user_following(user_instance))
print(user.user_followers(user_instance))
```

<details>
  <summary>Click to expand <code>user_following</code> & <code>user_followers</code> methods response</summary>

```json
{
    "ppark": {
        "display_name": "ppark"
    },
    "ryanshubert": {
        "display_name": "ryanshubert"
    },
    "crescendohouse": {
        "display_name": "Crescendo House"
    },...
}
   "ppark": {
        "display_name": "ppark"
    },
    "joacogarcia2023": {
        "display_name": "joacogarcia2023"
    },
    "ryanshubert": {
        "display_name": "ryanshubert"
    },...
}
```
</details>

<h2 id="user_films">user_films(user object)</h2>

```python
from letterboxdpy import user
user_instance = user.User("nmcassa")
print(user.user_films(user_instance))
```

<details>
    <summary>Click to expand the demo response for <code>user_films</code> method or <a href="/examples/exports/users/nmcassa/user_films.json" target="_blank">view the full response</a></summary>

```json
{
    "movies": {
        "godzilla-minus-one": {
            "name": "Godzilla Minus One",
            "id": "845706",
            "rating": 10,
            "liked": true
        },
        "flcl": {
            "name": "FLCL",
            "id": "284640",
            "rating": null,
            "liked": true
        },...
    },
    "count": 528,
    "liked_count": 73,
    "rating_count": 493,
    "rating_average": 6.43,
    "rating_percentage": 93.37,
    "liked_percentage": 13.83
}
```
</details>

<h2 id="user_reviews">user_reviews(user object)</h2>

```python
from letterboxdpy import user
user_instance = user.User("nmcassa")
print(user.user_reviews(user_instance))
```

<details>
  <summary>Click to expand <code>user_reviews</code> method response</summary>

```json
{
    "reviews": {
        "495592379": {
            "movie": {
                "name": "Poor Things",
                "slug": "poor-things-2023",
                "id": "710352",
                "release": 2023,
                "link": "https://letterboxd.com/film/poor-things-2023/"
            },
            "type": "Watched",
            "no": 0,
            "link": "https://letterboxd.com/nmcassa/film/poor-things-2023/",
            "rating": 6,
            "review": {
                "content": "It looks like AI art and weird movie",
                "spoiler": false
            },
            "date": {
                "year": 2023,
                "month": 12,
                "day": 26
            },
            "page": 1
        },
        "152420824": {
            "movie": {
                "name": "I'm Thinking of Ending Things",
                "slug": "im-thinking-of-ending-things",
                "id": "430806",
                "release": 2020,
                "link": "https://letterboxd.com/film/im-thinking-of-ending-things/"
            },
            "type": "Watched",
            "no": 0,
            "link": "https://letterboxd.com/nmcassa/film/im-thinking-of-ending-things/",
            "rating": 8,
            "review": {
                "content": "yeah i dont get it",
                "spoiler": false
            },
            "date": {
                "year": 2021,
                "month": 2,
                "day": 14
            },
            "page": 1
        }
    },
    "count": 7,
    "last_page": 1
}
```
</details>

<h2 id="user_diary">user_diary(user object)</h2>

```python
from letterboxdpy import user
user_instance = user.User("nmcassa")
print(user.user_diary(user_instance))
```

<details>
    <summary>Click to expand the demo response for <code>user_diary</code> method or <a href="/examples/exports/users/nmcassa/user_diary.json" target="_blank">view the full response</a></summary>

```json
{
    "entrys": {
        "513520182": {
            "name": "Black Swan",
            "slug": "black-swan",
            "id": "20956",
            "release": 2010,
            "runtime": 108,
            "rewatched": false,
            "rating": 9,
            "liked": true,
            "reviewed": false,
            "date": {
                "year": 2024,
                "month": 1,
                "day": 15
            },
            "page": 1
        },...
        ...},
        "129707465": {
            "name": "mid90s",
            "slug": "mid90s",
            "id": "370451",
            "release": 2018,
            "runtime": 86,
            "rewatched": false,
            "rating": 8,
            "liked": false,
            "reviewed": false,
            "date": {
                "year": 2020,
                "month": 10,
                "day": 20
            },
            "page": 7
        }
    },
    "count": 337,
    "last_page": 7
}
```
</details>

<h2 id="user_wrapped">user_wrapped(user object)</h2>

```python
from letterboxdpy import user
user_instance = user.User("nmcassa")
print(user.user_wrapped(user_instance, 2023))
```

<details>
    <summary>Click to expand the demo response for <code>user_wrapped</code> method or <a href="/examples/exports/users/nmcassa/user_wrapped.json" target="_blank">view the full response</a></summary>

```json
{
    "year": 2023,
    "logged": 120,
    "total_review": 2,
    "hours_watched": 223,
    "total_runtime": 13427,
    "first_watched": {
        "332289592": {
            "name": "The Gift",
            "slug": "the-gift-2015-1",
            "id": "255927",
            "release": 2015,
            "runtime": 108,
            "actions": {
                "rewatched": false,
                "rating": 6,
                "liked": false,
                "reviewed": false
            },
            "date": {
                "year": 2023,
                "month": 1,
                "day": 1
            },
            "page": {
                "url": "https://letterboxd.com/nmcassa/films/diary/for/2023/page/3/",
                "no": 3
            }
        }
    },
    "last_watched": {
        "495592379": {...}
    },
    "movies": {
        "495592379": {
            "name": "Poor Things",
            "slug": "poor-things-2023",
            "id": "710352",
            "release": 2023,
            "runtime": 141,
            "actions": {
                "rewatched": false,
                "rating": 6,
                "liked": false,
                "reviewed": true
            },
            "date": {
                "year": 2023,
                "month": 12,
                "day": 26
            },
            "page": {
                "url": "https://letterboxd.com/nmcassa/films/diary/for/2023/page/1/",
                "no": 1
            }
        },...
    },
    "months": {
        "1": 21,
        "2": 7,
        "3": 7,
        "4": 6,
        "5": 11,
        "6": 9,
        "7": 15,
        "8": 11,
        "9": 5,
        "10": 9,
        "11": 7,
        "12": 12
    },
    "days": {
        "1": 18,
        "2": 14,
        "3": 9,
        "4": 17,
        "5": 14,
        "6": 27,
        "7": 21
    },
    "milestones": {
        "50": {
            "413604382": {
                "name": "Richard Pryor: Live in Concert",
                "slug": "richard-pryor-live-in-concert",
                "id": "37594",
                "release": 1979,
                "runtime": 78,
                "actions": {
                    "rewatched": false,
                    "rating": 7,
                    "liked": false,
                    "reviewed": false
                },
                "date": {
                    "year": 2023,
                    "month": 7,
                    "day": 13
                },
                "page": {
                    "url": "https://letterboxd.com/nmcassa/films/diary/for/2023/page/1/",
                    "no": 1
                }
            }
        },
        "100": {
            "347318246": {...}
        }
    }
}
```
</details>

<h2 id="user_activity">user_activity(user object)</h2>

```python
from letterboxdpy import user
user_instance = user.User("nmcassa")
print(user.user_activity(user_instance))
```

<details>
    <summary>Click to expand the demo response for <code>user_activity</code> method or <a href="/examples/exports/users/nmcassa/user_activity.json" target="_blank">view the full response</a></summary>

```json
{
  "user": "nmcassa",
  "logs": {
    "6302725458": {
      "event_type": "basic",
      "time": {
        "year": 2024,
        "month": 1,
        "day": 30,
        "hour": 4,
        "minute": 7,
        "second": 42
      },
      "log_type": "watched",
      "title": "nmcassa   watched and rated  PlayTime   \u2605\u2605\u2605\u2605  on Monday Jan 29, 2024",
      "film": "PlayTime"
    },
    "6171883694": {
        "event_type": "review",
        "time": {
            "year": 2024,
            "month": 1,
            "day": 29,
            "hour": 12,
            "minute": 59,
            "second": 59
        },
        "event": "review",
        "type": "watched",
        "title": "nmcassa watched",
        "film": "example movie name",
        "film_year": 2000,
        "rating": 10,
        "spoiler": true,
        "review": "example review"
    },
    "6263706885": {
      "event_type": "basic",
      "time": {
        "year": 2024,
        "month": 1,
        "day": 23,
        "hour": 14,
        "minute": 32,
        "second": 12
      },
      "log_type": "liked",
      "title": "nmcassa liked L\u00e9o Barbosa\u2019s \ud83c\udfc6 Oscars 2024 list",
      "username": "000_leo"
    },...
}
```
</details>

<h2 id="user_lists">user_lists(user object)</h2>

```python
from letterboxdpy import user
user_instance = user.User("nmcassa")
print(user.user_lists(user_instance))
```

<details>
  <summary>Click to expand <code>user_lists</code> method response</summary>

```json
{
  "lists": {
    "30052453": {
      "title": "DEF CON Movie List",
      "slug": "def-con-movie-list",
      "description": "The DEF CON Hacking Conference's suggested movie list. defcon.org/html/links/movie-list.html",
      "url": "https://letterboxd.com/nmcassa/list/def-con-movie-list/",
      "count": 11,
      "likes": 0,
      "comments": 0
    }
  },
  "count": 1,
  "last_page": 1
}
```
</details>

<h2 id="user_watchlist">user_watchlist(user object)</h2>

```python
from letterboxdpy import user
user_instance = user.User("nmcassa")
watchlist_result = user.user_watchlist(user_instance, {'genre':['action','-drama']})
print(watchlist_result)
```

<details>
  <summary>Click to expand <code>user_watchlist</code> method response</summary>

```json
{
  "available": true,
  "count": 57,
  "data_count": 6,
  "last_page": 1,
  "filters": {
    "genre": [
      "action",
      "-drama"
    ]
  },
  "data": {
    "51397": {
      "name": "From Dusk Till Dawn",
      "slug": "from-dusk-till-dawn",
      "no": 6,
      "page": 1,
      "url": "https://letterboxd.com/films/from-dusk-till-dawn/"
    },...
    "62780": {
      "name": "Mad Max: Fury Road",
      "slug": "mad-max-fury-road",
      "no": 1,
      "page": 1,
      "url": "https://letterboxd.com/films/mad-max-fury-road/"
    }
  }
}
```
</details>

<h2 id="user_tags">user_tags(user object)</h2>

```python
from letterboxdpy import user
user_instance = user.User("nmcassa")
result = user.user_tags(user_instance)
print(result)
```

<details>
  <summary>Click to expand <code>user_tags</code> method response</summary>

```json
{
  "films": {"tags": {"lol": {...}}, "count": 1},
  "diary": {"tags": {"lol": {...}}, "count": 1},
  "reviews": {"tags": {"lol": {...}}, "count": 1},
  "lists": {
    "tags": {
      "hacking": {
        "name": "hacking",
        "title": "hacking",
        "link": "/nmcassa/tag/hacking/lists/",
        "count": 1,
        "no": 1
      }
    },
    "count": 1
  },
  "count": 4
}
```
</details>

<h1 id="Members">Members Objects</h1>

[To be documented.](https://github.com/search?q=repo:nmcassa/letterboxdpy+MemberListing)

<h2 id="top_users">top_users(members object)</h2>

[To be documented.](https://github.com/search?q=repo:nmcassa/letterboxdpy+top_users)

<h1 id="Movie">Movie Objects</h1>

```python
from letterboxdpy import movie
movie_instance = movie.Movie("v-for-vendetta")
print(movie_instance)
```

<details>
  <summary>Click to expand <code>Movie</code> object response</summary>

```json
{
    "url": "https://letterboxd.com/film/v-for-vendetta",
    "tmdb_link": "https://www.themoviedb.org/movie/752/",
    "poster": "https://a.ltrbxd.com/resized/film-poster/5/1/4/0/0/51400-v-for-vendetta-0-230-0-345-crop.jpg",
    "rating": 3.83,
    "year": 2005,
    "description": "In a world in which Great Britain has become a fascist state, a masked vigilante known only as \u201cV\u201d conducts guerrilla warfare against the oppressive British government. When V rescues a young woman from the secret police, he finds in her an ally with whom he can continue his fight to free the people of Britain.",
    "directors": [
        "James McTeigue"
    ],
    "genres": [
        "Thriller",
        "Science Fiction",...
    ],
    "popular_reviews": [
        {
            "reviewer": "zoey luke",
            "rating": " \u2605\u2605\u2605\u2605\u00bd ",
            "review": "I love natalie Portman and I hate the government"
        },
        {
            "reviewer": "shay",
            "rating": " \u2605\u2605\u2605\u2605\u2605 ",
            "review": "i'm like natalie portman in this film because after watching this i, too, became bald."
        },...
    ]
}
```
</details>

<h2 id="movie_details">movie_details(movie object)</h2>

```python
from letterboxdpy import movie
movie_instance = movie.Movie("v-for-vendetta")
print(movie.movie_details(movie_instance))
```

<details>
  <summary>Click to expand <code>movie_details</code> method response</summary>

```json
{
    "Country": [
        "Germany",
        "UK",
        "USA"
    ],
    "Studio": [
        "Virtual Studios",
        "Anarchos Productions",
        "Silver Pictures",
        "F\u00fcnfte Babelsberg Film",
        "Warner Bros. Productions",
        "DC Vertigo"
    ],
    "Language": [
        "English"
    ]
}
```
</details>

<h2 id="movie_watchers">movie_watchers(movie object)</h2>

```python
from letterboxdpy import movie
movie_instance = movie.Movie("v-for-vendetta")
print(movie.movie_watchers(movie_instance))
```

```json
{
    "watch_count": "981721",
    "fan_count": "8389",
    "like_count": "248662",
    "review_count": "35360",
    "list_count": "86666"
}
```

<h1 id="List">List Objects</h1>

```python
from letterboxdpy import list
list = list.List("Horrorville", "The Official Top 25 Horror Films of 2022")
print(list)
```

<details>
  <summary>Click to expand <code>List</code> object response</summary>

```json
{
    "title": "the-official-top-25-horror-films-of-2022",
    "author": "horrorville",
    "url": "https://letterboxd.com/horrorville/list/the-official-top-25-horror-films-of-2022/",
    "description": "To be updated monthly. It's ranked by average Letterboxd member rating. See the official top 50 of 2021 on Horrroville here. Eligibility rules: \u2022\u00a0Feature-length narrative films included only. \u2022\u00a0Shorts, documentaries, and TV are excluded. \u2022\u00a0Films must have their festival premiere in 2022 or their first national release in any country in 2022. \u2022\u00a0Films must have the horror genre tag on TMDb and Letterboxd. \u2022\u00a0There is a 1,000 minimum view threshold. Curated by Letterboxd Head of Platform Content Jack Moulton.",
    "filmCount": 25,
    "movies": [
        [
            "Nope",
            "/film/nope/"
        ],...
}
```
</details>

<h2 id="list_tags">list_tags(list object)</h2>

```python
from letterboxdpy import list
a = list.List("Horrorville", "The Official Top 25 Horror Films of 2022")
print(list.list_tags(a))
```

```python
['official', 'horror', 'letterboxd official', 'letterboxd', '2022', 'topprofile', 'top 25']
```

## Stargazers over time
[![Stargazers over time](https://starchart.cc/nmcassa/letterboxdpy.svg?background=%2300000000&axis=%23848D97&line=%23238636)](https://starchart.cc/nmcassa/letterboxdpy)