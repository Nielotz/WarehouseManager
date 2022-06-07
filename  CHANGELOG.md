# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Entry format ({} - optional):<br>
{⬜/✅} {[TYPE]} Change {[estimate]} {comments}<br>
Where type is in { FEATURE, API, FRONTEND, BACKEND }

## Planned

### Added

- [FEATURE] Swagger [5]
- [FEATURE] Loging in + keeping session [8]
- [FEATURE] Signing in [3]
- [FRONTEND] Improve CSS of the main page 1/2 [8] Prettify select item with
  arrow https://amethystwebsitedesign.com/wp-content/uploads/2014/11/dashicons-arrows-680-w.png
- [FRONTEND] Add "+" buttons [3]

## Planned 0.2.0 - 2022-06-06 - "We need to gain control"

### Added
- ⬜ [API] Support for addition / deletion of data (POST, DELETE) (Storage, Container, Item)
- ⬜ [FRONTEND] Support for addition / deletion of data (API call) (Storage, Container, Item)
    - ⬜ [FRONTEND] Support for adding data entry (Storage, Container, Item)
    - ⬜ [FRONTEND] Support for deleting data entry (Storage, Container, Item)

## Unreleased 0.1.0 - 2022-05-30 - "Just open eyes"

### Added

- ✅ [FEATURE] Support for selecting storages / containers - MultiLevelSelectList
    - ✅ [FRONTEND] Fetch storages and containers names
    - ✅ [FRONTEND] Display and allow selection of given storage / container
- ⬜ [FEATURE] Support for displaying items
    - ⬜ [API] New endpoint "/api/storage/\<storage>/container/\<container>/items"
    - ⬜ [FRONTEND] Fetch Items using API call
    - ⬜ [FRONTEND] Display received Items in table on the main page
    - ⬜ [BACKEND] API GET calls return data from DB (Storage, Container, Item)
        - ⬜ [BACKEND] Connect to DB
- ✅ Move database creation to backend

## 0.0.0 - 2022-05-29

### Added

- [FEATURE] This changelog
- [API] Dummy API endpoints - serve static data (Storage, Container, Item)
- [FRONTEND] Basic frontend of main page with static data