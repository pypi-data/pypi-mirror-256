# gemmail-python: A Gemmail (and Gembox) Parser for Misfin Clients and Servers

A parser written in python for gemtext, gemmails, and gemboxes, to be used with the Misfin(B) and Misfin(C) formats.

A Note On PEP-8: PEP-8 is a style guide for the Python standard library ONLY, as detailed in the official PEP-8 document:
> This document gives coding conventions for the Python code comprising the standard library in the main Python distribution.

Requiring that all programmers use the exact same style guide as the Python standard library is stupid and makes absolutely no sense. Other people's libraries should follow a consistent style within their own code, but they should not be forced to use a style of irrelevant code that's not part of their own library.

Erroring out on blank lines, not having two whitespaces before each function and class definition, and other such things DOES NOT CATCH ERRORS AND DOES NOT MAKE YOUR CODE BETTER. It is purely so Python developers can spend their time writing "clean code" instead of good code that does stuff. Nobody cares that you were able to put two blank lines before each function definition, what people care about is that your library actually implements stuff and works. Blank lines are not code, they do nothing. They do not help nor hinder your code.

Also, having two blank lines before a function definition instead of one blank line doesn't make your code more readable. That is BS, and I think every sane person knows that it is BS.

## GemMail

Parses the raw metadata and message data transmitted over the wire in the Misfin(B) and Misfin(C) protocols.

### Create GemMail
* GemMail() - creates an empty GemMail
* createGemMailFromBody(body) - creates GemMail from message body alone (metadata is not passed in)
* parseGemMail_B(gemmail_b_text) - parses the text in Misfin(B) format. Text should include the metadata.
* parseGemMail_C(gemmail_c_text) - parses the text in Misfin(C) format. Text should include the 3 lines of metadata at the beginning of the text.

### GemMail Values
* gm.ID - Identifier (if used with gembox, the Message ID)
* gm.Subject - the Subject of the message. Also included in gm.GemText.
* gm.Senders - GemMailSender array
* gm.Receivers - dictionary of addresses as keys, empty tuples as values.
* gm.Timestamps - datetime array
* gm.Tags - tags dictionary, may be used with GMAP and gembox.
* gm.GemText - GemText instance containing the lines of the message body, including the Subject line. Use `gm.GemText.string()` to convert just the message body to a string.

### GemMail Methods
* deepcopy() - deep copy GemMail to a new value
* containsSender(address) - checks if address is in senders list. Returns a boolean.
* setGemTextBody(gemtext_string) - parses the gemtext string and sets the GemMail's message body to it.
* prependSender(address, blurb) - prepends a sender to the senders list. Use this on the misfin server when a mail is received.
* appendSender(address, blurb) - appends a sender to the senders list.
* removeSender(address) - unimplemented.
* prependTimestamp(datetime) - prepends datetime value to timestamps list. Use this on the misfin server when a mail is received.
* appendTimestamp(datetime) - appends datetime value to timestamps list.
* containsReceiver(address) - checks if address is in recipients list. Returns a boolean.
* addReceiver(address) - adds a receiver to the recipients list.
* hasTag(tagName) - returns bool whether message has a tag and the tag's value is set to True.
* addTag(tagName) - adds a tag to the message, setting its value to true and its last_modification_date to datetime.utcnow()
* setTag(tagName, last_modification_date, value) - sets a tag's data manually
* removeTag(tagName) - untags a message by setting its value to False and its last_modification_date to datetime.utcnow()

* string_C() - returns a string of the gemmail in Misfin(C) format, ready to be transmitted over the wire using the Misfin(C) protocol.
* string_B() - returns a string of the gemmail in Misfin(B) format, ready to be transmitted over the wire using the Misfin(B) protocol.

### Example Usage
```python
from gemmail_python import *

text_misfinC = """clseibold@auragem.letz.dev Christian Lee Seibold

2023-10-04T08:26:32Z
# Message Subject Line

Message body.
"""
gemmail = gemmail_python.parseGemmail_C(text_misfinC)
gemmail.prependSender(sender_address, sender_blurb)
newGemmailString = gemmail.string_B() # Converts to Misfin(B) format for transmission via Misfin(B) protocol
```

## GemBox

Parses a gembox file in the new format (or in the deprecated formats). See [NewGemBoxFormat.md](NewGemBoxFormat.md) for the format specification.

### Create a GemBox
* GemBox(identifier) - create empty GemBox. Identifier is for programmer's use to identify gemboxes.
* parseGemBox() - parses gembox file in new format.

Deprecated:
* parseGemBox_B_old(identifier, textString) - parses gembox file in deprecated format for Misfin(B)
* parseGemBox_C_old(identifier, textString) - parses gembox file in deprecated format for Misfin(C)

### GemBox Values
* Identifier - an identifier to be used by the programmer
* MailboxAddress - from Mailbox metadata field
* MailboxBlurb - from Mailbox metadata field
* Fingerprint - from Fingerprint metadata field
* Description - from Description metadata field
* CreatedTags - dictionary of CreatedTags metadata field
* Mails - GemMail array

### GemBox Methods
* deepcopy() - deep copy GemBox to a new value
* getGemMailWithID(id) - returns the GemMail that has the provided ID, along with its index in the Mails array
* getGemMailsWithTag(tagName) - returns list of GemMails that have the provided tag
* appendGemMail(gemmail) - appends a GemMail instance to the Mails array
* removeGemMail(index) - removes a GemMail instance at the specified index from the Mails array.
* removeGemMailAtID(id) - removes a GemMail that has the provided ID.
* string() - returns a string of the GemBox to be written to a file, in new format.

Deprecated:
* string_B() - returns a string of the GemBox to be written to a file, in deprecated format for Misfin(B).
* string_C() - returns a string of the GemBox to be written to a file, in deprecated format for Misfin(C).

## Example Usage

```python
from gemmail_python import *

gembox_text = ""
gembox = gemmail_python.parseGemBox("", gembox_text)

# Add all Inbox mails to Archive folder
mails = gembox.getGemMailsWithTag("Inbox") # Get array of all mails with "Inbox" tag
for mail in mails:
    mail.addTag("Archive") # Automatically removes "Inbox" tag, since Archive and Inbox are mutually exclusive folder tags

print(gembox.string())
print(gembox.Mails[0].string_C()) # print first mail in misfin(C) wire format.
```

## GemText

Parses a Gemtext file (.gmi file) to be used with Gemini or the message body of a Gemmail.

### Create a GemText
* GemText() - empty gemtext
* parseGemText(text) - parses a gemtext file into a GemText instance

### GemText Values
* firstLevel1Heading - string of first level-1 heading of file, or None if doesn't appear in text. This may also be included in the lines array.
* lines - GemTextLine array

### GemText Methods
* deepcopy() - deep copy GemText to a new value
* string() - convert GemText instance back to a string.

## GemTextLine

A line within a Gemtext file.

### Create a GemTextLine
* GemTextLine(GemTextLineType, text, url)

### GemTextLine Values
* type - GemTextLineType
* text - string of text, excluding the linetype prefix
* url - string of url for Link line types

### GemTextLine Methods
* string() - Converts line to a string, including the linetype prefix.

### GemTextLineType Enum Values
* Text - regular text
* PreformattingToggle - preformat toggle line (\`\`\`)
* PreformattedText - text in between preformat toggle lines
* Link
* ListItem
* Heading1
* Heading2
* Heading3
* Quote - aka. Blockquote
