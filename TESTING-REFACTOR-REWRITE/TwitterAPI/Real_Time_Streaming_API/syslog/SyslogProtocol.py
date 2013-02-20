class SyslogProtocol:

    PRIORITY = {
        0: "emerg", 1: "alert", 2: "crit", 3: "err",
        4: "warning", 5: "notice", 6: "info", 7: "debug"
    }

    PRIORITY_REVERSE = {
        "emerg": 0, "alert": 1, "crit": 2, "err": 3,
        "warning": 4, "notice": 5, "info": 6, "debug": 7
    }

    FACILITY = {
        0: "kern", 1: "user", 2: "mail", 3: "daemon",
        4: "auth", 5: "syslog", 6: "lpr", 7: "news",
        8: "uucp", 9: "cron", 10: "authpriv", 11: "ftp",
        12: "ntp", 13: "security", 14: "console", 15: "mark",
        16: "local0", 17: "local1", 18: "local2", 19: "local3",
        20: "local4", 21: "local5", 22: "local6", 23: "local7"
    }

    @classmethod
    def facility(self, number):
        try: return self.FACILITY[number >> 3]
        except: return "unknown"

    @classmethod
    def priority(self, number):
        try: return self.PRIORITY[number & 0x07]
        except: return "unknown"

    @classmethod
    def decode(self, data):
        res = []
        for chunk in data.split("\n"):
            if not chunk:
                continue

            if chunk[2] == ">":
                res.append({
                    "facility": SyslogProtocol.facility(int(chunk[1])),
                    "priority": SyslogProtocol.priority(int(chunk[1])),
                    "message": chunk[3:]
                })
            elif chunk[3] == ">":
                res.append({
                    "facility": SyslogProtocol.facility(int(chunk[1:2])),
                    "priority": SyslogProtocol.priority(int(chunk[1:2])),
                    "message": chunk[4:]
                })
            elif chunk[4] == ">":
                res.append({
                    "facility": SyslogProtocol.facility(int(chunk[1:3])),
                    "priority": SyslogProtocol.priority(int(chunk[1:3])),
                    "message": chunk[5:]
                })
            else:
                res.append({
                    "facility": "unknown",
                    "priority": "unknown",
                    "message": chunk
                })
        return res

    @classmethod
    def encode(self, facility, priority, message):
        return "<%d>%s" % ((facility << 3) + priority, message)