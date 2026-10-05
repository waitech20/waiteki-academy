# WaiTeki Academy: maudhui ya masomo

Folda hii ndiyo inayopandishwa GitHub Pages. App inapakua kutoka hapa
`catalog.json` na `lessons/<lugha>.json`, kwa hiyo unaweza kuongeza somo bila
kutoa toleo jipya la app.

## Kupandisha mara ya kwanza

1. github.com -> **New repository**. Jina: `waiteki-academy`. Chagua **Public**
   (Pages ya bure inahitaji repo ya umma). Bonyeza **Create repository**.
2. **Add file -> Upload files**. Buruta `catalog.json` na folda `lessons`, kisha **Commit changes**.
3. Faili `.nojekyll` (tupu, jina linaanza na nukta) linaweza kukataa kupanda kwa kuburuta.
   Likikosekana: **Add file -> Create new file**, andika jina `.nojekyll`, kisha Commit.
4. **Settings -> Pages**. Source: **Deploy from a branch**. Branch: `main`, folda `/ (root)`. **Save**.
5. Subiri dakika 1 hadi 2. Anwani itakuwa:
   `https://JINA-LAKO.github.io/waiteki-academy`
6. Jaribu kwenye kivinjari: `https://JINA-LAKO.github.io/waiteki-academy/catalog.json`
   inatakiwa kuonyesha maandishi ya JSON. Ukiona 404, subiri kidogo au angalia hatua 4.

Kisha mpe Claude anwani hiyo (bila `/` mwishoni) ili aiweke kwenye `AcademyConfig.remoteBase`.

## Kuongeza somo jipya (mfano: Rust)

1. Weka `lessons/rust.json` (muundo ule ule wa `lessons/python.json`).
2. Endesha: `python3 tools/update_catalog.py`. Inakagua masomo na kusasisha
   `lessonCount`, `quizCount`, `freeLessons`, `proLessons`, `levels` na `updated`.
   Ukiona `ERROR`, rekebisha kwanza.
3. Pandisha `catalog.json` na `lessons/rust.json` GitHub (Commit).
4. Ndani ya dakika chache (GitHub Pages inahifadhi nakala kwa takriban dakika 10) somo linapatikana kwenye app.

Hakuna Python? Unaweza kuhariri `lessonCount` n.k. kwenye `catalog.json` kwa mkono. Lugha yenye `lessonCount` zaidi ya 0
ndiyo inayohesabiwa kuwa ina masomo (app na worker zote zinatumia kigezo hiki).

## Sheria za kukumbuka

- Jina la faili lazima liwe sawa na `id` ya lugha kwenye catalog (`rust` -> `lessons/rust.json`).
- Kila somo linahitaji: `id`, `language`, `level`, `title`, `access` (`free` au `pro`) na `quiz` isiyo tupu.
- `id` za masomo zisijirudie ndani ya faili moja.
- Usibadilishe `id` za masomo yaliyokwisha chapishwa: maendeleo ya watumiaji (XP, masomo yaliyokamilika) yanazitumia.
