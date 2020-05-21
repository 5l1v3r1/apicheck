---
layout: post
author: cr0hn
author_link: https://twitter.com/ggdaniel
title:  "Sending traffic to BurpSuite"
---

In the [previous post](https://bbva.github.io/apicheck/2020/05/08/save-navigation-sessions.html) post we talk about how to store a navigation traffic in a session file. Now we'll use this file to send to a proxy, like BurpSuite or OWASP ZAP Proxy
<!--more-->

As part of `APICheck tool set` there's available the [Send-to-proxy](https://bbva.github.io/apicheck/tools/apicheck/send-to-proxy) tool. This tool reads from stdin and send each [APICheck Data Objects](https://bbva.github.io/apicheck/docs/building-new-tools#apicheck-data-format) to a proxy.

By using the session file that we were generated in previous post we'll use it to send to [BurpSuite](https://portswigger.net):

First we check BurpSuite listen port BurpSuite:

![BurpSuite Config](https://i.ibb.co/SKyMcLk/burpsuite-listen-addr.png)

Then, we send session to proxy:

```bash
$ cat sessions.data| docker run --rm -it bbvalabs/apicheck-proxy http://127.0.0.1:9000
[*] Request sent: 'https://cr0hn.com:443/'
[*] Request sent: 'https://cr0hn.com:443/wp-includes/css/dist/block-library/style.min.css'
[*] Request sent: 'https://cr0hn.com:443/wp-includes/css/dist/block-library/theme.min.css'
[*] Request sent: 'https://cr0hn.com:443/wp-content/plugins/card-elements-for-elementor/assets/css/common-card-style.css'
[*] Request sent: 'https://cr0hn.com:443/wp-content/plugins/card-elements-for-elementor/assets/css/testimonial-card-style.css'
...
``` 

Now we check that all the requests were received by the proxy:

![BurpSuite received data](https://i.ibb.co/vzXLpk7/burpsuite-send-to-proxy.png)

