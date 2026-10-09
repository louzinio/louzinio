<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <img src="assets/banner-light.svg" alt="Yonatan Louzon - Practical Engineer, Navigation Warfare" width="100%">
</picture>

<br/>

I work on the part of navigation that starts when GPS stops being trustworthy — **detecting, characterizing and defeating GNSS jamming and spoofing**, and keeping position and time alive while someone is actively trying to take them away. Most of my work lives between the receiver, the RF bench and the tools that make sense of both.

<br/>

### Focus

| Area | Scope |
|---|---|
| **Electronic attack** | GNSS jamming and spoofing — detection, characterization, emitter localization |
| **Protection** | Anti-jam antennas (CRPA), null steering, interference mitigation |
| **Threat simulation** | GNSS simulators, live ephemeris pipelines, repeatable attack scenarios on the bench |
| **Timing** | 1PPS, GPSDO holdover and time-server integrity under threat |
| **Receivers** | JAVAD (GREIS), NovAtel (OEM), u-blox — raw logs, transcoding, bridging |

### Threat model

| Threat | Effect | Countermeasure |
|---|---|---|
| Jamming | Loss of lock, no fix | C/N₀ and AGC monitoring, J/S estimation, CRPA null steering, holdover |
| Spoofing | Position and time walked off silently | Multi-receiver cross-checks, clock and position jump detection, signal-power consistency |
| Meaconing | Delayed rebroadcast of real signals | Timing-residual analysis, 1PPS vs. disciplined oscillator |
| Denial | No GNSS at all | GPSDO holdover, alternate PNT, clear indication of when trust was lost |

### Tools

![Python](https://img.shields.io/badge/Python-24292f?style=flat-square&logo=python&logoColor=white) ![Rust](https://img.shields.io/badge/Rust-24292f?style=flat-square&logo=rust&logoColor=white) ![Qt](https://img.shields.io/badge/PySide6-24292f?style=flat-square&logo=qt&logoColor=white) ![Raspberry Pi](https://img.shields.io/badge/Raspberry_Pi-24292f?style=flat-square&logo=raspberrypi&logoColor=white) ![Linux](https://img.shields.io/badge/Linux-24292f?style=flat-square&logo=linux&logoColor=white) ![NMEA](https://img.shields.io/badge/NMEA-24292f?style=flat-square) ![RTCM](https://img.shields.io/badge/RTCM-24292f?style=flat-square) ![GREIS](https://img.shields.io/badge/GREIS-24292f?style=flat-square) ![NovAtel](https://img.shields.io/badge/NovAtel_OEM-24292f?style=flat-square) ![SCPI](https://img.shields.io/badge/SCPI-24292f?style=flat-square)

### Selected work

<a href="https://github.com/louzinio/javad-logger">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api/pin/?username=louzinio&repo=javad-logger&theme=github_dark&hide_border=true&bg_color=0d1117">
    <img src="https://github-readme-stats.vercel.app/api/pin/?username=louzinio&repo=javad-logger&hide_border=true&bg_color=f6f8fa" alt="javad-logger">
  </picture>
</a>

<br/>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api/top-langs/?username=louzinio&layout=compact&theme=github_dark&hide_border=true&bg_color=0d1117&langs_count=6">
  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=louzinio&layout=compact&hide_border=true&bg_color=f6f8fa&langs_count=6" alt="Languages">
</picture>
