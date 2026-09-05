# Haflati — project site

A bilingual (Arabic RTL / English LTR) startup site that lets a visitor *drive*
the product instead of watching a demo video.

## Pages

Five pages, hash-routed, all inside the one file:

    #/           الرئيسية      hero, the twin-phone simulator, the market
                               problem, how the money works, download
    #/about      من نحن        the origin story, four principles, the team,
                               and the road so far and ahead
    #/app        تطبيق العميل   fifteen screens with a picker, plus twelve
                               features covering the app and the map
    #/partners   تطبيق المزوّد  eleven screens with a picker, plus six features
    #/admin      لوحة الإدارة   the admin console in a browser frame, plus
                               the two-role permission split
    #/tech       التقنية        architecture, the six booking states, the
                               trust gates, and the deliberate decisions
    #/download                 the home page scrolled to its download section

Routing is hash-based on purpose: no server rewrites, works on any static host
and straight off the filesystem.

Below 1000px the top nav is replaced by a **horizontal section strip** rather
than a hamburger. An icon alone doesn't tell anyone there is more to look at —
the strip keeps all six sections visible and one tap away, and scrolls the
active chip into view on navigation. It sits in normal flow rather than sticking,
so it doesn't compete with the simulator's own pinned chrome further down the
home page. The drawer is still there for keyboard and screen-reader users but
the burger is hidden.

## The app pages behave differently on a phone

On desktop they're a sticky handset with a list of screens beside it — you click
a name, the phone changes, both stay in view.

That layout fails on a phone: the list sits *below* the handset, so every tap
scrolls you away from the thing you just changed. Below 900px the pages are
rebuilt as a **scrolling story** instead — each screen rendered in its own
handset with its title and description directly underneath, stacked top to
bottom. Nothing to tap, nothing to scroll back to. Real screenshots carry a
small "Real screenshot" marker in their caption.

The stack is built lazily, only when the viewport is actually narrow, so desktop
never pays for the extra 26 handset frames.

Section counts of the "60 endpoints / 34 migrations" kind were removed — they
read as a class assignment rather than a product.

## Files

    index.html            everything — markup, styles, script, every
                          screenshot AND both launch videos, all inlined.
                          Opens on its own from anywhere. No build step.
    assets/               the same launch clips as loose files, if you would
                          rather serve them separately
    downloads/            put the two APK files here (see downloads/README.txt)

`index.html` makes **zero external requests**. Copy that one file anywhere and
the whole site works, video included — verified by copying it alone into an
empty folder and loading it.

Each clip is inlined twice: **webm (VP9)** for Chrome, Firefox, Edge and Safari
16+, and **mp4 (H.264)** as the `<source>` fallback for anything older. The
browser picks whichever it can decode. A poster frame is inlined as well, so the
first paint shows the app rather than a black rectangle.

## The imagery is the app's own

Every photograph on the page comes from `Hafleti/assets/images/` — the same
bundle the app ships:

    decoration.jpg   the wedding hall listing and its booking thumbnails
    photography.jpg  the photography vendor and the photo-session listing
    deserts.jpg      the cake listing and the cake shop on the map
    Sham.png         the Sham Cash mark on the payment screen

The QR on the payment screen is real. It encodes
`5d81538eddf306614694b043054486e9` — the account ID from
`lib/core/widgets/sham_cash_qr.dart` — rendered at error-correction level L in
`#3A4A7B` on white, exactly as `ShamCashQr` draws it. It scans.

To swap in different photos, replace the matching entry in the `IMG` object at
the top of the `<script>` block with your own data URI or a URL.

## Running it

Open `index.html` in a browser. That is all — no server, no npm, no bundler.

## Hosting

Any static host works. Upload the whole folder as-is.

  * Netlify / Vercel — drag the folder onto the dashboard
  * GitHub Pages — push the folder, enable Pages on the branch
  * Cloudflare Pages — connect the repo, no build command, output = this folder

The only external request is Google Fonts (El Messiri, Cairo, Plus Jakarta Sans).
If the site must work fully offline, download those three families into
`assets/fonts/` and replace the `<link>` in `<head>` with local `@font-face` rules.

## Editing content

All visible text lives in one place: the `T` object near the top of the
`<script>` block. Every entry is `key:["العربية","English"]`, and every element
that shows text carries a matching `data-i18n="key"`. Change the pair, both
languages update. There are 231 keys and the site verifies at load that every
`data-i18n` reference has a dictionary entry.

Longer structured content sits in four arrays just below `T`:

    STEPS       the 7 steps of the twin-phone simulator
    MACHINE     the 6 booking states and their facts
    FEATURES    the per-app feature lists
    LED_NOTES   the ledger's explanatory note per stage

## Themes

The site ships light and dark, and the phones follow the site. The in-phone
colours are `AppColors`' own light and dark sets copied verbatim from
`lib/core/theme/app_colors.dart`, so switching the site theme shows the app
exactly as it renders in that mode — `#FAF7F8 / #FFFFFF / #E8DDE0 / #3E3135`
in light, `#1C161A / #271E23 / #402E36 / #F5ECEE` in dark.

Dark is the default. The choice is remembered in `localStorage` under
`haflati-theme`.

## The customer app page is entirely real captures

**Every screen on the site is now a real capture — both apps, no rebuilds left.**

`#/app` carries sixteen: Home, Explore, Filters, a product shop, a product page,
a service vendor, a service page, booking details, the vendor's portfolio,
paying the deposit, booking confirmed, Bookings & Orders, Saved, Messages,
writing a review, and a support request.

`#/partners` carries fourteen, covering **both vendor kinds**: Home, Booking
Requests (service), Product Orders (seller), an order's detail, the booking
calendar, My Products, editing a product, withdrawing to Sham Cash, My Portfolio,
Reviews, Chats, Notifications, Support, and Profile. They carry the app's real
data: Maria Flowers, Jane's Accessories, Velora Boutique, GLO&MORE, JoicusePPe,
حلويات الوسام.

**Each screen has a light and a dark capture.** `applyTheme` swaps the pair, so
flipping the site theme shows the app in the matching theme rather than a dark
screenshot on a light page. Keys are `sh_<name>L` and `sh_<name>D` in the `IMG`
object.

Captures are cropped to remove the OS status bar and gesture pill, resized to
400px wide, and the handset's aspect ratio matches them exactly — nothing is
cropped or letterboxed, and the notch hides itself on a capture.

To swap in a newer one, replace the matching `sh_*L` / `sh_*D` entry with a new
data URI. Every screen now has both halves of its pair.

The **vendor** page is still rebuilt from the Flutter source; captures from
`hafleti_partners` would replace those the same way.

## The phone mockups

The screens that are *not* screenshots are not images either. Every screen is rebuilt in HTML/CSS against the
actual Flutter widget source, so it stays crisp, animates, and can be edited:

    HomeHeaderWidget        menu + greeting + chat/bell circles with badges
    HomeSearchBarWidget     h50, r18, card fill + shadow, filter button
    HomeCategoriesWidget    60x60 tile, r20, primarySoft + border
    HomeVendorCardWidget    195x130 image, r20, pad 12/10/12/12
    HomeListingCardWidget   165x120 image, r18, pad 10/8/10/10,
                            discount pill top-start, rating badge on scrim
                            bottom-start, favourite circle top-end
    BottomNavView           the five real tabs and their labels
    HomeSpotlightCarousel   r24 card under the categories, 5.2s per slide,
                            dots (16x5 active / 5x5) bottom-start and a
                            2.5h progress rail, with the background scaling
                            as the slide advances
    HomeSpotlightSlide      kick chip, two-line title, meta line, then either
                            a white CTA pill in primaryDark or a hint row
    HomeSpotlightMapArtwork the explore slide's painted map — primaryDark to
                            accentDeep, streets tilted -0.3rad, three range
                            rings, satellite dots and a gold centre marker
    ExploreView             location bar with the radius label, category chips,
                            a results bar with the map/list toggle, the map at
                            r22 with a zoom control, the user's own position
                            dot and vendor pins that carry a name plate, then
                            ExploreVendorStrip scrolling sideways beneath it

Wording comes from the apps' own `assets/translations/ar.json` and `en.json`
wherever a key exists, so the mock reads as the shipped UI does — `مرحباً ريم`,
`المزودون الأعلى تقييماً`, `بانتظار موافقة مزوّد الخدمة`, `دُفع العربون`.

The vendor screens come from `hafleti_partners` at `af63ed1` "Final release
version" — the shipped build, where every feature is API-connected. Ten screens:
service home, bookings with local filters, booking detail with the response
window, the full-day blocking calendar, listings, wallet with held vs available,
portfolio, reviews with the star breakdown, chat inbox and conversation, and
profile with the settings rows.

Sources for those: `EarningsCardWidget` (r20, primary gradient, 30sp amount),
`StatisticsWidget` (four counters with hairline dividers), `BookingRequestWidget`,
`BalanceCard`, `TransactionTile`, `ServiceTileWidget`, `FilterBar`, and the
booking calendar from §23 of that repo's own CLAUDE.md, where the unit is a whole
day and booked days are read-only.

## On mobile

Three columns can't sit side by side on a phone, so below 900px the stage is
rebuilt in three pieces:

1. **A switcher**, pinned under the top bar. It follows the story on its own —
   it moves to the vendor when the vendor is the one acting — and puts a gold
   dot on the other tab when that side's screen also changed on this step, so
   nothing happens off-screen unannounced.
2. **A swipeable track**, pinned below the switcher. The two handsets sit in a
   scroll-snap row; swipe between them and the tabs follow. Because the phone is
   sticky, it never scrolls away while you are reading or tapping.
3. **A control bar fixed to the bottom of the screen**, holding the caption, the
   back/next arrows, and the seven steps as a horizontal strip that scrolls the
   active step into view. It slides up only while the stage is in view.

The ledger scrolls normally between the two, so it is never in the way.

Two bugs worth recording, because both were invisible until measured:

* `position:sticky` was silently dead because `.stage` had `overflow:hidden`.
* `position:fixed` on the control bar anchored to `.stage` rather than the
  viewport, because the stage's entrance animation left a transform on it and a
  transformed ancestor becomes the containing block. The stage now fades in with
  opacity only.
* The swipe track used `overflow-x:auto`, which quietly makes an element a
  *vertical* scroll container as well — so a vertical swipe starting on the phone
  was swallowed instead of scrolling the page. `overflow-y:hidden` plus
  `overscroll-behavior-y:auto` fixes it.

## The design

Palette is taken from the logo itself — the gold ribbon, the rose crescent, the
white letterforms — on the app's own dark theme, deepened. Gold is reserved for
money and appears nowhere else. Type is the apps' own stack: El Messiri for
Arabic display, Cairo for Arabic body, Plus Jakarta Sans for English and all
figures.

The centrepiece is the twin-phone stage: the customer's phone and the vendor's
phone run the same booking at the same time, with the ledger between them. It
exists to show the one thing a screen recording cannot — that after payment the
vendor's 85% is *visible but held*, and only releases when the event completes.

## Accessibility

Keyboard operable throughout, visible focus rings, a skip link, `prefers-reduced-motion`
respected, live regions on the simulator caption and the state-machine detail,
and `lang`/`dir` swapped correctly on language change.


## The admin console page

Built from the console file itself, not from a description. That file is a
bundled single-page app; unpacking it (base64 → gzip → seventeen `text/babel`
modules) gives the real structure, which the mockup follows:

* sidebar groups exactly as `AdminSidebar` defines them — Dashboard, then
  **Operations** (Vendors, Users, Bookings, Complaints, Moderation), then
  **Finance** (Money, Financials) and **System** (Audit log, Admins)
* the live badges it computes: vendors where `!is_approved`, complaints not
  `resolved`, and cancelled bookings with `refund_amount > 0 && !refund_paid`
* the role chip, and the `cap` gating that hides Finance and System from a
  support account
* the eight `StatCard`s in their tones, and the twelve-month profit trend

## Support, on both sides

The two apps treat support differently and the site now shows both:

* **Customer** — a *ticket* system, not a chat. Four categories (payment, no
  show, vendor behaviour, other), a subject, an optionally attached booking,
  and three statuses: awaiting reply, in review, resolved.
* **Vendor** — a permanent thread with the Haflati team, and the only route to
  cancelling a booking once it has been approved.

## A correction worth recording

The vendor bottom bar is not a flat five-tab bar. `VendorBottomNav` has r24 top
corners and a **raised 50r circular gradient button** in the middle for listings,
with two normal tabs either side: Home, Bookings/Orders — [listings] — Chats,
Profile. There is no wallet tab; the wallet is reached by tapping the earnings
card on the home screen. The earlier build had this wrong.


## Team names

Names **and roles** are hardcoded Latin with `dir="ltr"` and are deliberately
*not* in the translation dictionary — both read identically in Arabic and
English. To edit either, find `<h4 dir="ltr">` and `<span class="role">` in the
about page.

## Phone sizing

The handset scales with the viewport rather than sitting at a fixed small width:
`min(272px, 78vw)` in the simulator and `min(300px, 84vw)` on the app pages,
below 900px. The simulator's is checked against the fixed control bar so the
bottom of the screen is never hidden behind it — pinned, the phone occupies
63→655px of an 844px viewport, with the bar starting at 736.


## Two cascade traps worth remembering

Both bit during this build and neither throws an error:

* An override written *above* the rule it overrides silently loses. It happened
  twice — the mobile step strip, and the masthead clearance. Anything that has
  to win now lives at the end of the stylesheet.
* `overflow-x:hidden` on `body` makes body the scrollport for `position:sticky`,
  so sticky elements stop pinning. It was removed once the breakpoint sweep
  confirmed there is no horizontal overflow to hide.


## Four simulations, one handset each

The earlier version put both apps side by side with a ledger between them. That
was wrong for two reasons: on a phone only one handset fits, so the second was
always off-screen, and pairing them forced the payment step to jump straight to
the vendor before you had read the customer's screen.

It is now **one handset, one path**, chosen by two segmented controls — side ×
kind:

    تطبيق العميل  ×  طلب منتج    7 steps · browse → shop → product → pay →
                                  await reply → in touch → review
    تطبيق العميل  ×  حجز خدمة    8 steps · browse → service vendor → service →
                                  date & add-ons → deposit → confirmed →
                                  waiting → review
    تطبيق المزوّد ×  طلب منتج    6 steps · notification → product orders →
                                  order detail → accept & talk → review →
                                  withdraw
    تطبيق المزوّد ×  حجز خدمة    6 steps · notification → booking requests →
                                  the date locks → in touch → review → withdraw

Both vendor paths end on **withdrawing to Sham Cash**, so the money's journey is
shown from the customer's pocket to the vendor's wallet.

## The money strip, and why it is not sticky

The ledger became a single row of states — لم يُدفع بعد · عند حفلتي · محجوز
للمزوّد · متاح للسحب · غادر إلى شام كاش — lighting the current one and dimming
those already passed.

Making it sticky on a phone was tried and abandoned. The pinned block was almost
as tall as its own container, so it had nowhere to travel and slid away after a
hundred pixels — worse than not pinning at all. The simulator is now **sized to
fit one screen**: the handset takes `min(100dvh - 356px, 62vh)`, and the strip
and caption sit under it. Nothing scrolls inside the section, so nothing can
disappear. Measured at 360×740, 390×844 and 430×932 — the strip and caption are
fully visible at all three.

## One capture still missing its pair

`sh_vmyproductsD` exists but `sh_vmyproductsL` does not, so My Products falls
back to the dark capture in light theme. Add it to the `IMG` object and it slots
straight in.

## The pay step hands over by itself

Both flows mark their payment step `auto:true`. Landing on it shows the
customer's Pay Deposit screen, waits three seconds, then advances — which makes
the vendor the acting side and, on a phone, slides the switcher across to his
handset. Any manual move (a step tap, the arrows, or switching flow) cancels the
pending hand-over, and it is skipped entirely under `prefers-reduced-motion`.

Both flows now end on **the vendor withdrawing to Sham Cash**, so the money's
journey is shown end to end: the customer pays into Haflati, the split is
recorded, the vendor's share is held, it releases on completion, and only at the
final step does it leave the platform.

## Two class collisions, same lesson

Cloned app screens share a stylesheet with the page around them, so generic
class names collide:

* `.cap` — the portfolio tiles inside a cloned screen used it, and so did the
  mobile stack's caption. Renamed to `.st-cap`.
* `.live` — the simulator marks the acting side with it, and the tappable screen
  button was given the same name. `#sideC` picked up `position:absolute` and
  escaped the grid. Renamed to `.tapscreen`.

Anything new inside a phone frame should take a prefixed name.


## The mobile top nav, again

Pill chips in a horizontal scroller read as dated and as something to swipe past.
It is now a **flush tab row with an underline** — six equal-width labels, no
icons, no scrolling, the active one in rose with a rose rule beneath it. Labels
are shortened on small screens (`navUserShort` and friends) so all six fit a
360px viewport without truncation.


## The hero plays the app launching

The opening is no longer a static mock: a handset beside the headline plays a
**real recording of the app starting up** — the logo animating in over
"Elegance in Every Detail", then the home screen filling in from skeletons.
There is a light recording and a dark one, and `applyTheme` swaps the pair along
with everything else.

Encoded at 440px wide, **30fps**, 9 seconds, muted, looping, `playsinline`. The
dark clip starts 0.3s in so it opens on the logo rather than a black frame.

## The vendor page, reordered

Product Orders and Notifications were removed. The remaining thirteen run in the
order a vendor actually meets them, with the profile second rather than buried
at the end:

    Home · Profile · Booking Requests · Order detail · Booking calendar ·
    My Products · Editing a product · My Portfolio · The wallet ·
    Withdrawing to Sham Cash · Reviews · Chats · Support

Both vendor simulations now open on Home — an order or a booking simply appearing
— rather than on a notification, and both pass through **the wallet** before the
withdrawal, so you see the amount move from pending to available before it leaves.


## Screenshot quality

All 56 screenshots are encoded at **600px wide, JPEG q74, 4:2:0**. That is the
balance point: 600px at 4:2:0 costs about the same bytes as 480px at 4:4:4 while
carrying 25% more resolution, which matters because the handset renders at up to
300 CSS px and therefore 600 device px on a 2× display.

## The admin console has four views

Like the two app pages, it now has a picker: the dashboard, reviewing a vendor,
money owed, and an open complaint. The console's own sidebar is wired to the
same views, so clicking المزوّدون or الأموال in the mockup moves it too.

## A flex trap worth recording

The money strip is a horizontal scroller inside a flex column. Two defaults
broke it, and neither threw an error:

* `min-width:auto` on a flex item meant the scroller refused to shrink and
  pushed the whole page 100px wider than the viewport.
* `align-items:center`, inherited from the desktop grid rule, made the flex
  children size to their content rather than the container — so the fix above
  had no effect until alignment was set back to `stretch`.
