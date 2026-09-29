"""Plain-language help page. Written for people who have never heard of PXE."""
from ui import e, icon

def _step(n, title, done, body, open_=False):
    mark = f'<span class="num ok">{icon("check", 14)}</span>' if done else f'<span class="num">{n}</span>'
    return f'<details class="card gd" {"open" if open_ else ""}><summary>{mark}{title}</summary><div class="gb">{body}</div></details>'

def _faq(q, a):
    return f'<details class="gq"><summary>{q}</summary><div class="gb">{a}</div></details>'

def guide_body(ip, iface, up, img, has_farm, n_rigs, any_seen, acked, n_done):
    tip = lambda t: f'<div class="tip">{t}</div>'
    warn = lambda t: f'<div class="tip warn">{t}</div>'
    prog = f'<div class="card"><h2>Your progress: {n_done} of 6 steps done</h2><div class="meter"><i style="width:{n_done * 100 // 6}%"></i></div>' \
           f'<p class="hint" style="margin:0">Open a step below and follow it. Green ticks appear by themselves as you finish each one.</p></div>'

    intro = f"""<div class="card"><h2>What does this app do?</h2>
<p>Normally you install Hive OS on a mining rig by writing it to a USB stick or drive, one rig at a time.
This app lets your rigs <b>install Hive OS by themselves over your home network</b>. You turn a rig on, it asks this server for
Hive OS, installs it on its own disk, and joins your Hive account. Do it once for one rig or for fifty.</p>
<p><b>What you need:</b></p><ul>
<li>This machine (the computer running this app), connected to your router with a network cable (Wi-Fi is not recommended).</li>
<li>Each mining rig connected to the <b>same router</b> with a network cable, and with its own disk (SSD) inside.</li>
<li>A free Hive OS account with a farm created.</li>
<li>A keyboard and screen for each rig, <b>once</b>, to change one setting in its BIOS (Step 5).</li></ul>
{warn("<b>Important:</b> a rig that is flashed has its disk <b>erased</b>. Only rigs you add to the Rigs list are ever touched. Other computers on your network are ignored.")}</div>"""

    s1 = _step(1, "Give this machine a permanent address", acked, f"""
<p>Rigs find this server by its address on your network. Routers sometimes hand out a new address after a restart, which would make the
rigs look in the wrong place. Ask your router to always give this machine the <b>same</b> address:</p>
<p>This machine's address right now: <b class="mono">{e(ip)}</b> <button class="copy" data-copy="{e(ip)}" title="Copy">{icon("copy", 14)}</button></p>
<ol><li>Open your router's settings page in a browser (often <code>192.168.1.1</code> or <code>192.168.0.1</code>; the address and password are usually on a sticker on the router).</li>
<li>Look for a menu called <b>DHCP reservation</b>, <b>Address reservation</b>, <b>Static lease</b> or <b>Reserved IP</b>.</li>
<li>Choose this machine from the list of devices (or type its address above) and save.</li>
<li>Come back here and press <b>"I've done this"</b> on the Dashboard.</li></ol>
{tip("Router menus look different on every brand. If you cannot find it, search the internet for <i>your router brand + DHCP reservation</i>.")}
""", open_=not acked)

    s2 = _step(2, "Get the Hive OS image", bool(img), f"""
<p>The <b>image</b> is the Hive OS file that gets installed on each rig. You only need to get it once.</p>
<ol><li>On the Hive OS website (hiveos.farm), open the download page and find the newest <b>Hive OS image</b>.
It is a large file ending in <code>.img.xz</code>. <b>Do not unzip it.</b></li>
<li>Right-click the download button, choose <b>Copy link address</b>.</li>
<li>Open the <a href="/images">Image</a> tab here, paste the link into <b>Download from a link</b>, and press <b>Download</b>.
A progress bar shows while it downloads (it is several gigabytes, so give it a few minutes).</li>
<li>When it is finished it shows <b>Active</b>. If you have more than one image, press <b>Use this</b> on the one you want.</li></ol>
{tip("Already downloaded the file to your computer? On the Image tab, drag it into the <b>Upload a file</b> box instead.")}
{f'<p>Current image: <b>{e(img)}</b></p>' if img else ''}
""", open_=bool(acked) and not img)

    s3 = _step(3, "Tell the app about your Hive farm", has_farm, f"""
<p>A <b>Farm Hash</b> is a code that links your rigs to your Hive OS account. With it, every rig you flash shows up in your account on its own,
with no typing on the rig.</p>
<ol><li>Log in to the Hive OS website and open your <b>farm</b>.</li>
<li>Open the farm's <b>Settings</b> and look for <b>Farm Hash</b> (menu names can change a little over time). Copy it.</li>
<li>Open the <a href="/groups">Groups</a> tab, paste it into <b>Farm hash</b>, and press <b>Save</b>.</li></ol>
<p>Leave the other boxes alone unless you know you need to change them. <b>Hive API URL</b> is already correct for normal Hive OS accounts.</p>
{tip("<b>What is a group?</b> A group is a set of rigs that share the same settings. Most people only ever need the one called <b>default</b>.")}
""")

    s4 = _step(4, "Add your rigs to the list", n_rigs > 0, f"""
<p>Tell the app which machines it is allowed to install Hive OS on. Each rig needs a <b>name</b> and its <b>MAC address</b>.</p>
<p><b>What is a MAC address?</b> A unique ID of the rig's network port, like <span class="mono">AA:BB:CC:DD:EE:FF</span>.
Ways to find it:</p><ul>
<li>A <b>sticker</b> on the motherboard or next to the network port.</li>
<li>Your <b>router's device list</b> (shows every connected device with its MAC).</li>
<li>Easiest: <b>turn the rig on once with network boot enabled (Step 5)</b>. Its screen shows a line such as <i>CLIENT MAC ADDR</i>. Write it down, then add it here.</li></ul>
<p>Then open the <a href="/rigs">Rigs</a> tab, fill in <b>Name</b> and <b>MAC address</b>, and press <b>Add rig</b>.
Have many rigs? Use <b>Import a list</b> and paste one rig per line, like <code>rig01 aa:bb:cc:dd:ee:01</code>.</p>
{tip("<b>Static IP (optional):</b> leave it <b>blank</b> unless you want a rig to always have the same address. If you fill it in, it must fit your network, for example <code>192.168.1.51</code>. Blank means the rig gets its address from your router as usual.")}
""")

    s5 = _step(5, "Set each rig to start from the network", any_seen, """
<p>A rig normally starts from its own disk. You need to tell it to look at the network first. You do this <b>once per rig</b>.</p>
<ol><li>Connect a keyboard and screen to the rig and power it on.</li>
<li>Right away, tap the BIOS key over and over. It is usually <b>Delete</b> or <b>F2</b> (sometimes F10, F12 or Esc). The screen briefly shows which one.</li>
<li>Find the <b>Boot</b> settings. Turn on options called <b>Network Boot</b>, <b>PXE</b>, <b>LAN Boot</b> or <b>Network Stack</b> (turn on IPv4 PXE if you see that choice).</li>
<li>Set the <b>boot order</b> so the <b>network / LAN</b> option is <b>first</b>, then the disk.</li>
<li>Save and exit (usually <b>F10</b>).</li></ol>
<p>BIOS screens differ a lot between motherboards. If you get lost, search the internet for <i>your motherboard name + enable PXE boot</i>.</p>
""" + tip("Do not worry about leaving network boot first. After a rig is installed, this server tells it to start from its own disk automatically."))

    s6 = _step(6, "Turn the rig on and watch it install", n_done >= 6, f"""
<ol><li>Make sure the <a href="/">Dashboard</a> says <b>Deploy server: Running</b>.</li>
<li>Power on the rig. After a few seconds it shows network boot text, then a short message like <i>Hive deploy: flashing rig01</i>.</li>
<li>On the Dashboard the rig changes to <b>Flashing</b> with a moving progress bar. This usually takes <b>10 to 20 minutes</b>.</li>
<li>When done, the rig <b>restarts by itself</b> and the Dashboard shows <b>Deployed</b>. In a few minutes it appears in your Hive OS account.</li></ol>
{warn("Do <b>not</b> turn the rig off while it says Flashing.")}
<p><b>Later:</b> to install again on a rig, press the circular-arrow <b>Reflash</b> button next to it in the Rigs tab, then restart the rig.
If a rig already has Hive OS working and you just want to track it, press <b>Mark as deployed</b> (the skip icon) so it is not erased.</p>
""")

    trouble = """<div class="card"><h2>Something is not working?</h2>""" + "".join([
        _faq("The rig does not try to boot from the network",
             "<ul><li>Check the network cable is plugged into the rig <b>and</b> your router.</li><li>Re-check Step 5: network boot must be enabled <b>and</b> first in the boot order.</li>"
             "<li>Make sure the Dashboard says <b>Running</b>. If it says <b>Stopped</b>, open <a href='/settings'>Settings</a> and press <b>Restart dnsmasq</b>.</li>"
             "<li>Confirm the rig is in the <a href='/rigs'>Rigs</a> list with the right MAC address.</li></ul>"),
        _faq("The rig starts its old system instead of installing",
             "<ul><li>The rig may be marked <b>Deployed</b> already. Press <b>Reflash</b> in the Rigs tab, then restart it.</li><li>Its MAC address may be typed wrong in the list.</li><li>No image is selected. Check the <a href='/images'>Image</a> tab shows one as <b>Active</b>.</li></ul>"),
        _faq("The rig shows Failed",
             "<ul><li>Look at <b>Activity</b> on the Dashboard for the reason.</li><li>The rig needs <b>internet access</b> while installing, not just your home network.</li>"
             "<li>The rig needs an internal disk of at least 7 GB. If it has more than one disk, open <a href='/groups'>Groups</a> and type the right one in <b>Target disk</b> (for example <code>/dev/sda</code>). Leave it blank to let the app choose.</li>"
             "<li>Press <b>Reflash</b> to try again.</li></ul>"),
        _faq("The rig installed but is not in my Hive OS account",
             "<ul><li>Wait 5 minutes and refresh your Hive OS page.</li><li>Check the <b>Farm hash</b> in Groups for typos or spaces, and that the rig is in that group.</li><li>The rig needs internet access to reach Hive OS.</li></ul>"),
        _faq("The rig got a different network address than I typed",
             "<p>Addresses typed in the Rigs tab are applied when the rig is installed. If you change one later, press <b>Reflash</b> to apply it.</p>"),
        _faq("The Dashboard says Stopped",
             "<p>Another program on this machine may be using the same network ports. Press <b>Restart dnsmasq</b> in Settings. If it keeps stopping, look at the <b>dnsmasq log</b> at the bottom of the Dashboard and share it when asking for help.</p>"),
        _faq("I forgot my password",
             "<p>On this machine, delete the file <code>app-data/HiveOSPXE-hive-os-pxe/data/config.json</code> and restart the app. The password goes back to the one shown with this app when you installed it. "
             "<b>This also clears your rig list</b>, so download a backup first from Settings when you can.</p>"),
    ]) + "</div>"

    safety = """<div class="card"><h2>Good to know</h2><ul>
<li><b>Safe by design:</b> only devices in your Rigs list are installed on. Unknown devices always start normally.</li>
<li><b>Your home router stays in charge.</b> This app never hands out network addresses, so it cannot break your Wi-Fi or internet.</li>
<li><b>Keep it at home.</b> Never open ports on your router for this app. It is only meant to be used inside your own network.</li>
<li><b>Back up:</b> Settings has an <b>Export configuration</b> button that saves your rigs and groups.</li></ul></div>"""

    gloss = """<div class="card"><h2>Words you may see</h2><dl class="gl">
<dt>PXE / network boot</dt><dd>A rig starting up by asking the network for its software instead of reading its own disk.</dd>
<dt>Image</dt><dd>The Hive OS file that is copied onto each rig's disk.</dd>
<dt>Flashing</dt><dd>Copying the image onto the rig's disk. This erases what was on the disk.</dd>
<dt>MAC address</dt><dd>The permanent ID of a network port, used to recognise each rig.</dd>
<dt>Farm hash</dt><dd>A code that connects rigs to your Hive OS account automatically.</dd>
<dt>Static IP</dt><dd>An address a rig always keeps. Optional.</dd>
<dt>Group</dt><dd>Rigs that share the same network and Hive settings.</dd>
<dt>BIOS</dt><dd>The settings screen you can open when a computer first turns on.</dd></dl></div>"""

    return prog + intro + s1 + s2 + s3 + s4 + s5 + s6 + trouble + safety + gloss
