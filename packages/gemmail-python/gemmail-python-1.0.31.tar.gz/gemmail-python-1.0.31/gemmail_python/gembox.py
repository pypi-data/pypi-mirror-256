from .gemmail import *
from io import StringIO
import iso8601
import copy

class GemBox:
    Identifier = "" # For your use
    MailboxAddress = ""
    MailboxBlurb = ""
    Fingerprint = ""
    Description = ""

    def __init__(self, identifier):
        self.Identifier = identifier
        self.Mails = []
        self.CreatedTags = {}

    def deepcopy(self):
        result = GemBox()
        for mail in self.Mails:
            result.Mails.append(mail.deepcopy())
        result.Identifier = copy.copy(self.Identifier)
        result.MailboxAddress = copy.copy(self.MailboxAddress)
        result.MailboxBlurb = copy.copy(self.MailboxBlurb)
        result.Fingerprint = copy.copy(self.Fingerprint)
        result.Description = copy.copy(self.Description)
        result.CreatedTags = copy.deepcopy(self.CreatedTags)
        return result
    
    def getGemMailWithID(self, id): # Returns mail and its index in the Mails array
        for index, mail in enumerate(self.Mails):
            if mail.ID == id:
                return mail, index
        return None, -1

    def getGemMailsWithTag(self, tagName): # Returns list of gemmails that have that tag
        result = []
        for mail in self.Mails:
            if mail.hasTag(tagName):
                result.append(mail)
        return result

    def appendGemMail(self, gemmail):
        self.Mails.append(gemmail)

    def removeGemMail(self, index):
        self.Mails = self.Mails[:index] + self.Mails[index + 1:]
    
    def removeGemMailByID(self, id):
        _, index = self.getGemMailWithID(id)
        if index != -1:
            self.removeGemMail(index)
    
    def string(self):
        result = StringIO()

        # Gembox Metadata (if exists)
        if self.MailboxAddress != "":
            result.write(f"Mailbox: {self.MailboxAddress}")
            if self.MailboxBlurb != "":
                result.write(f" {self.MailboxBlurb}")
            result.write("\n")
        if self.Description != "":
            result.write(f"Description: {self.Description}\n")
        if self.Fingerprint != "":
            result.write(f"Fingerprint: {self.Fingerprint}\n")
        
        if len(self.CreatedTags) > 0:
            result.write("CreatedTags: ")
            for index, tag in enumerate(self.CreatedTags):
                if tag == "":
                    continue
                if index > 0:
                    result.write(",")
                result.write(tag)
            result.write("\n")
        
        # Gembox Messages
        for index, mail in enumerate(self.Mails):
            # Message ID
            result.write(f"[{mail.ID}]\n")

            # Metadata
            if len(mail.Senders) > 0:
                result.write("Senders: ")
                for index, s in enumerate(mail.Senders):
                    if s.address == "":
                        continue
                    if index > 0:
                        result.write(",")
                    result.write(s.address)
                    if s.blurb != "":
                        result.write(f" {s.blurb}")
                result.write("\n")
            
            if len(mail.Receivers) > 0:
                result.write("Recipients: ")
                for index, k in enumerate(mail.Receivers):
                    if k == "":
                        continue
                    if index > 0:
                        result.write(",")
                    result.write(k)
                result.write("\n")
            
            if len(mail.Timestamps) > 0:
                result.write("Timestamps: ")
                for index, t in enumerate(mail.Timestamps):
                    if index > 0:
                        result.write(",")
                    result.write(t.strftime('%Y-%m-%dT%H:%M:%SZ'))
                result.write("\n")
            
            # Tags
            if len(mail.Tags) > 0:
                for tagName, tagData in mail.Tags.items():
                    result.write(f"{tagName}: ")
                    result.write(tagData.last_modification_date.strftime('%Y-%m-%dT%H:%M:%SZ'))
                    if tagData.value:
                        result.write(" true\n")
                    else:
                        result.write(" false\n")
            
            # Message Subject and Body
            if mail.Subject == None:
                result.write("#\n")
            result.write(mail.GemText.string())
        return result.getvalue()
            

    def string_B_old(self): # Deprecated
        result = StringIO()
        for index, mail in enumerate(self.Mails):
            if index > 0:
                result.write("<=====\n")
            result.write(mail.string_B())
        return result.getvalue()

    def string_C_old(self): # Deprecated
        result = StringIO()
        for index, mail in enumerate(self.Mails):
            if index > 0:
                result.write("<=====\n")
            result.write(mail.string_C())
        return result.getvalue()

def parseGemBox(identifier, gembox_text = ""):
    lines = gembox_text.splitlines(False)
    result = GemBox(identifier)

    inGboxMetadata = True # Very start of file is the metadata for the whole gembox
    inBody = False
    bodyStart = 0
    currentGemMail = GemMail(None)
    for index, line in enumerate(lines):
        if line.startswith("["): # Start of new message data
            if not inGboxMetadata and currentGemMail.ID != None:
                # End of message body, append message to GemBox
                currentGemMail.setGemtextBody('\n'.join(lines[bodyStart:index]) + '\n')
                result.appendGemMail(currentGemMail)

            # Start of new message metadata, parse message ID
            msgID = line.removeprefix("[").removesuffix("]")
            currentGemMail = GemMail(msgID)
            inBody = False
            inGboxMetadata = False
        elif inBody and line.startswith("\\["): # Escaped bracket in message body, unescape it
            lines[index] = "[" + line.removeprefix("\\[")
        elif inGboxMetadata:
            if line.startswith("Mailbox:"):
                mailbox = line.removeprefix("Mailbox:").lstrip()
                mailbox_parts = mailbox.split(" ", 1)
                if len(mailbox_parts) == 1:
                    result.MailboxAddress = mailbox_parts[0]
                elif len(mailbox_parts) == 2:
                    result.MailboxAddress = mailbox_parts[0]
                    result.MailboxBlurb = mailbox_parts[1]
            elif line.startswith("Fingerprint:"):
                fingerprint = line.removeprefix("Fingerprint:").strip()
                result.Fingerprint = fingerprint
            elif line.startswith("Description:"):
                description = line.removeprefix("Description:").lstrip()
                result.Description = description
            elif line.startswith("CreatedTags:"):
                createdTags = line.removeprefix("CreatedTags:").strip()
                tags = createdTags.split(",")
                for tag in tags:
                    tag = tag.strip()
                    result.CreatedTags[tag] = ()
        else:
            if line.startswith("Senders:"):
                senders = line.removeprefix("Senders:").split(",")
                for s in senders:
                    s = s.lstrip()
                    if s == "":
                        continue
                    parts = s.split(None, 1)
                    if len(parts) == 1:
                        currentGemMail.appendSender(parts[0], "")
                    elif len(parts) == 2:
                        currentGemMail.appendSender(parts[0], parts[1])
            elif line.startswith("Recipients:"):
                recipients = line.removeprefix("Recipients:").split(",")
                for r in recipients:
                    r = r.strip()
                    if r == "":
                        continue
                    currentGemMail.addReceiver(r)
            elif line.startswith("Timestamps:"):
                timestamps = line.removeprefix("Timestamps:").split(",")
                for t in timestamps:
                    t = t.strip()
                    if t == "":
                        continue
                    dt = iso8601.parse_date(t)
                    currentGemMail.appendTimestamp(dt)
            elif line.startswith("#"): # Subject Line - Start of gemtext body
                inBody = True
                bodyStart = index
            else: # Tags
                # TODO: Make sure tag is in CreatedTags field first?
                parts = line.split(":", 1)
                if len(parts) == 2:
                    tagName = parts[0].strip()
                    tagValueParts = parts[1].strip().split(None)
                    last_modification_date_timestamp = iso8601.parse_date(tagValueParts[0])
                    value = False
                    if tagValueParts[1] == "true" or tagValueParts == "True" or tagValueParts == "TRUE":
                        value = True
                    currentGemMail.setTag(tagName, last_modification_date_timestamp, value)
    
    # Add last gemmail
    if currentGemMail.ID != None:
        # End of message body, append message to GemBox
        currentGemMail.setGemtextBody('\n'.join(lines[bodyStart:len(lines)]))
        result.appendGemMail(currentGemMail)
    
    return result


def parseGemBox_B_old(identifier, gembox_text = ""): # Deprecated
    result = GemBox(identifier)
    gembox_text_length = len(gembox_text)

    current_start = 0
    while current_start < gembox_text_length:
        final = False
        current_end = gembox_text.find("<=====", current_start)
        if current_end == -1:
            current_end = gembox_text_length
        
        text = gembox_text[current_start:current_end]
        gm = parseGemMail_B(text)
        result.appendGemMail(gm)

        current_start = gembox_text.find("\n", current_end) + 1
    return result

def parseGemBox_C_old(identifier, gembox_text = ""): # Deprecated
    result = GemBox(identifier)
    gembox_text_length = len(gembox_text)

    current_start = 0
    while current_start < gembox_text_length:
        final = False
        current_end = gembox_text.find("<=====", current_start)
        if current_end == -1:
            current_end = gembox_text_length
        
        text = gembox_text[current_start:current_end]
        gm = parseGemMail_C(text)
        result.appendGemMail(gm)

        # new line after "<=====" string
        sep_newline = gembox_text.find("\n", current_end)
        if sep_newline == -1:
            break
        current_start = sep_newline + 1
    return result
