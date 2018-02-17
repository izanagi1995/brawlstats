# Band
A full band object to get a band's statistics.

### Attributes

| Name | Type |
|------|------|
| `tag` | str |
| `id.high` | int |
| `id.low` | int |
| `name` | str |
| `status` | str |
| `band_members_count` | int |
| `band_trophies` | int |
| `band_required_trophies` | int |
| `band_description` | str |
| `band_members` | List\[[Member](https://github.com/SharpBit/abrawlpy/blob/master/docs/member.md), [Member](https://github.com/SharpBit/abrawlpy/blob/master/docs/member.md)\] |

# Simple Band
Only returns some statistics of the band.

### Attributes
| Name | Type |
|------|------|
| `band_name` | str |
| `band_tag` | str |
| `band_trophies` | int |
| `band_required_trophies` | int |
| `members_count` | int |
| `maybe_player_role` | int |
