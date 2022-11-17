with genres as (
    select
        g.created,
        g.modified,
        g.name,
        gfw.film_work_id
    from content.genre g
             left join content.genre_film_work gfw
                       on gfw.genre_id = g.id
),
 agg_genre as (
     select
         g.film_work_id,
         json_agg(g.name) as "genres"
     from genres g
     group by
         g.film_work_id
 ),
 persons as (
     select
         p.full_name,
         pfw.film_work_id,
         pfw.role,
         p.id,
         p.created,
         p.modified
     from content.person p
              left join content.person_film_work pfw
                        on p.id = pfw.person_id
 ),
 all_directors as (
     select distinct
         persons.film_work_id,
         first_value(persons.id) over (partition by persons.film_work_id) as "person_id"
     from persons
     where persons.role = 'director'
     group by persons.film_work_id, persons.id
 ),
 directors as (
     select distinct
         all_directors.film_work_id, persons.full_name
     from all_directors, persons
     where all_directors.person_id=persons.id
 ),
 writers as (
     select
         persons.film_work_id,
         json_agg (
                 json_build_object(
                         'id'::text, persons.id::text,
                         'full_name'::text, persons.full_name::text
                     )
             ) as "writers"
     from persons
     where persons.role = 'writer'
     group by persons.film_work_id

 ),
 actors as (
     select
         persons.film_work_id,
         json_agg (
                 json_build_object(
                         'id', persons.id,
                         'full_name', persons.full_name
                     )
             ) as "actors"
     from persons
     where persons.role = 'actor'
     group by persons.film_work_id
 ),
 actors_names as (
     select
         persons.film_work_id,
         json_agg (
                 persons.full_name::text
             )
             as "actors_names"
     from persons
     where persons.role = 'actor'
     group by persons.film_work_id
 ),
 writers_names as (
     select
         persons.film_work_id,
         json_agg (
                 persons.full_name::text
             )
             as "writers_names"
     from persons
     where persons.role = 'writers'
     group by persons.film_work_id
 ),
 ids as (
     select id
     from content.film_work f
     where
        f.modified > '01.01.2022'
        or f.created > '01.01.2022'
     union
     select p.film_work_id as "id"
     from persons p
     where
        p.modified > '01.01.2022'
        or p.created > '01.01.2022'
     union
     select g.film_work_id as "id"
     from genres g
     where
        g.modified > '01.01.2022'
        or g.created > '01.01.2022'
 )

select
    json_build_object('id', fw.id,
                      'imdb_rating', coalesce(fw.rating,0),
                      'title', fw.title,
                      'description', coalesce(fw.description, ''),
                      'director', coalesce(directors.full_name, ''),
                      'writers', coalesce(writers.writers,'[]'),
                      'actors', coalesce(actors.actors,'[]'),
                      'actors_names', coalesce(actors_names.actors_names,'[]'),
                      'genres', coalesce(agg_genre.genres,'[]')) as "xyz"
from content.film_work fw
         left join directors on directors.film_work_id = fw.id
         left join writers on writers.film_work_id = fw.id
         left join actors on actors.film_work_id = fw.id
         left join actors_names on actors_names.film_work_id = fw.id
         left join writers_names on writers_names.film_work_id = fw.id
         left join agg_genre on agg_genre.film_work_id = fw.id
where fw.id in (select id from ids)

