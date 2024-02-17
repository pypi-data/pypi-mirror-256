from .gemtext import *
import datetime
from io import StringIO
import iso8601
import copy


class GemMailSender:
    address = ""
    blurb = ""
    def __init__(self, address, blurb):
        self.address = address
        self.blurb = blurb


class GemMailTag:
    tag = ""
    last_modification_date = None
    value = False

    def __init__(self, tag, last_modification_date, value = False):
        self.tag = tag
        self.last_modification_date = last_modification_date
        self.value = value


class GemMail:
    ID = ""
    Subject = None # None if subject was never set (doesn't occur in message body), otherwise a string

    def __init__(self, ID) -> None:
        self.ID = ID
        self.Senders = []
        self.Receivers = {}
        self.Timestamps = []
        self.Tags = {}
        self.GemText = GemText()

    def deepcopy(self):
        result = GemMail()
        result.Subject = copy.copy(self.Subject)
        result.Senders = copy.deepcopy(self.Senders)
        result.Receivers = copy.deepcopy(self.Receivers)
        result.Timestamps = copy.deepcopy(self.Timestamps)
        result.GemText = self.GemText.deepcopy()
        result.Tags = copy.deepcopy(self.Tags)
        return result
    
    def containsSender(self, address):
        for s in self.Senders:
            if s.address == address:
                return True
        return False
    
    def setGemtextBody(self, gemtext):
        self.GemText = parseGemText(gemtext)
        self.Subject = self.GemText.firstLevel1Heading

    def prependSender(self, address, blurb):
        self.Senders.insert(0, GemMailSender(address, blurb))

    def appendSender(self, address, blurb):
        self.Senders.append(GemMailSender(address, blurb))

    def removeSender(self, address):
        pass

    def prependTimestamp(self, datetime):
        self.Timestamps.insert(0, datetime)

    def appendTimestamp(self, datetime):
        self.Timestamps.append(datetime)

    def containsReceiver(self, address):
        return address in self.Receivers

    def addReceiver(self, address):
        self.Receivers[address] = ()

    def hasTag(self, tagname):
        if self.Tags.__contains__(tagname):
            return self.Tags.get(tagname).value
        return False

    def addTag(self, tagname):
        if tagname == "Inbox":
            self.removeTag("Archive")
            self.removeTag("Drafts")
            self.removeTag("Sent")
        elif tagname == "Archive":
            self.removeTag("Inbox")
            self.removeTag("Drafts")
            self.removeTag("Sent")
        elif tagname == "Drafts":
            self.removeTag("Inbox")
            self.removeTag("Archive")
            self.removeTag("Sent")
        elif tagname == "Sent":
            self.removeTag("Inbox")
            self.removeTag("Archive")
            self.removeTag("Drafts")
        last_modification_date = datetime.datetime.utcnow()
        self.Tags[tagname] = GemMailTag(tagname, last_modification_date, True)

    def setTag(self, tagname, last_modification_date, value):
        self.Tags[tagname] = GemMailTag(tagname, last_modification_date, value)

    def removeTag(self, tagname):
        last_modification_date = datetime.datetime.utcnow()
        if self.Tags.__contains__(tagname):
            self.Tags[tagname].last_modification_date = last_modification_date
            self.Tags[tagname].value = False

    def string_C(self):
        # Write metadata to top of file, in first 3 lines
        result = StringIO()

        # First line is senders
        for index, s in enumerate(self.Senders):
            if s.address == "":
                continue
            if index > 0:
                result.write(",")
            result.write(s.address)
            if s.blurb != "":
                result.write(f" {s.blurb}")
        result.write("\n")
        
        # Second line is recipients
        for index, k in enumerate(self.Receivers):
            if k == "":
                continue
            if index > 0:
                result.write(",")
            result.write(k)
        result.write("\n")

        # Third line is timestamps in RFC3339 format
        for index, t in enumerate(self.Timestamps):
            if index > 0:
                result.write(",")
            result.write(t.strftime('%Y-%m-%dT%H:%M:%SZ'))
        result.write("\n")

        # Write the rest of the message body
        result.write(self.GemText.string())

        return result.getvalue()
    
    def string_B(self):
        # Write metadata to top of file
        result = StringIO()

        # Senders
        for _, s in enumerate(self.Senders):
            if s.address == "":
                continue
            result.write(f"< {s.address}")
            if s.blurb != "":
                result.write(f" {s.blurb}")
            result.write("\n")
        
        # Recipients
        for index, k in enumerate(self.Receivers):
            if k == "":
                continue
            if index > 0:
                result.write(",")
            result.write(k)
        result.write("\n")

        # Timestamps
        for index, t in enumerate(self.Timestamps):
            result.write("@ ")
            result.write(t.strftime('%Y-%m-%dT%H:%M:%SZ'))
            result.write("\n")

        # Write the rest of the message body
        result.write(self.GemText.string())

        return result.getvalue()


# Create GemMail from message body alone. Metadata is not passed in.
def createGemMailFromBody(body):
    return parseGemMail_B(body)


def parseGemMail_B(gemmail_text = "") -> GemMail:
    spacetab = " \t"
    lines = gemmail_text.splitlines(False)
    result = GemMail()

    pre = False
    for line in lines:
        line = line.strip()

        if line.startswith("```"):
            pre = not pre
        elif pre:
            pass
        elif line.startswith("<"):
            line = line.removeprefix("<").strip()
            parts = line.split(" ", 1)
            sender = GemMailSender()
            if len(parts) == 1:
                sender = GemMailSender(parts[0], "")
            else:
                sender = GemMailSender(parts[0], parts[1])
            result.Senders.append(sender)
        elif line.startswith(":"):
            line = line.removeprefix(":").strip()
            parts = line.split(" ")
            for part in parts:
                result.Receivers[part] = ()
        elif line.startswith("@"):
            line = line.removeprefix("@").strip()
            dt = iso8601.parse_date(line)
            result.Timestamps.append(dt)
    result.GemText = parseGemText(gemmail_text)
    result.Subject = result.GemText.firstLevel1Heading
    return result


def parseGemMail_C(gemmail_text = ""):
    spacetab = " \t"
    lines = gemmail_text.splitlines(False)
    result = GemMail()

    pre = False
    for index, line in enumerate(lines):
        # Parse the first 3 lines, which are static, in the order of senders, recipients, timestamps
        if index == 0: # Senders list
            senders = line.split(",")
            for s in senders:
                s = s.lstrip()
                if s == "":
                    continue
                parts = s.split(None, 1)
                if len(parts) == 1:
                    gml = GemMailSender(parts[0], "")
                    result.Senders.append(gml)
                elif len(parts) == 2:
                    gml = GemMailSender(parts[0], parts[1])
                    result.Senders.append(gml)
        elif index == 1: # Recipients list
            recipients = line.split(",")
            for r in recipients:
                r = r.strip()
                if r == "":
                    continue
                result.Receivers[r] = ()
        elif index == 2: # Timestamps list
            timestamps = line.split(",")
            for t in timestamps:
                t = t.strip()
                if t == "":
                    continue
                dt = iso8601.parse_date(t)
                result.Timestamps.append(dt)
    result.GemText = parseGemText('\n'.join(lines[3:]))
    result.Subject = result.GemText.firstLevel1Heading
    return result
