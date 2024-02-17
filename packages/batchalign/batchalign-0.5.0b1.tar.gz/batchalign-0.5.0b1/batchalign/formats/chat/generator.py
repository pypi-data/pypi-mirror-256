from batchalign.document import *
from batchalign.constants import *

import warnings

# c = CHATFile("./extern/test.cha")
# document = c.doc

# document[0].model_dump()
# document[3].text = None
# document[3].model_dump()

def generate_chat_utterance(utterance: Utterance):
    """Converts at Utterance to a CHAT string.

    Parameters
    ----------
    utterance : Utterance
        The utterance to be written to string.

    Returns
    -------
    str
        The generated string.
    """
    
    main_line = str(utterance)
    tier = utterance.tier

    mors = []
    gras = []
    has_wor = False
    wor_elems = []

    for i in utterance.content:
        mors.append(i.morphology)
        gras.append(i.dependency)
        if i.time:
            has_wor = True
            wor_elems.append(f"{i.text} \x15{str(i.time[0])}_{str(i.time[1])}\x15")
        else:
            wor_elems.append(i.text)

        if bool(mors[-1]) != bool(gras[-1]):
            warnings.warn(f"Batchalign has detected a mismatch between lengths of mor and gra tiers for utterance; output will not pass CHATTER; line='{main_line}'")


    # assemble final output
    result = [f"*{tier.id}:\t"+main_line]

    #### MOR LINE GENERATION ####
    # we need to first join every MWT with ~
    mor_elems = []
    for mor in mors:
        if mor != None:
            # I'm sorry. This is just mor line generation; there is actually not that much complexity here
            mor_elems.append("~".join(f"{m.pos}|{m.lemma}{'-' if any([m.feats.startswith(i) for i in UD__GENDERS]) else ('-' if m.feats else '')}{m.feats}"
                                    for m in mor))
    if len(mor_elems) > 0:
        # if the end is punct, drop the tag
        if mor_elems[-1].startswith("PUNCT"):
            mor_elems[-1] = mor_elems[-1].split("|")[1]
        result.append("%mor:\t"+" ".join(mor_elems))

    #### GRA LINE GENERATION ####
    # gra list is not different for MWT tokens so we flatten it
    gras = [i for j in gras if j for i in j]
    # assemble gra line
    gra_line = None
    if len(gras) > 0:
        result.append("%gra:\t"+" ".join([f"{i.id}|{i.dep_id}|{i.dep_type}" for i in gras]))

    #### WOR LINE GENERATION ####
    if has_wor:
        result.append("%wor:\t"+" ".join(wor_elems))


    #### EXTRA LINE GENERATION ####
    for special in utterance.custom_dependencies:
        if special.content:
            result.append(f"%{special.id}:\t"+special.content)

    return "\n".join(result)

def generate_chat_preamble(doc, birthdays=[]):
    """Generate header for a Batchalign document.

    Parameters
    ----------
    doc : Document
        The document to generate a CHAT header.
    birthdays : List[CustomLine]
        A list of custom lines for which the id mentions "Birthday"
        (It's apparently a CHAT requirement to put them right after @ID)

    Returns
    -------
    str
        The generated CHAT preamble.
    """
    
    header = []
    header.append("@Languages:\t"+", ".join(doc.langs))
    header.append("@Participants:\t"+", ".join([f"{i.id} {i.name}" for i in doc.tiers]))
    header.append("@Options:\tmulti")
    header.append("\n".join([f"@ID:\t{i.lang}|{i.corpus}|{i.id}|{i.birthday}|{i.additional[0]}|{i.additional[1]}|{i.additional[2]}|{i.name}|{i.additional[3]}|{i.additional[4]}|" for i in doc.tiers]))
    for i in birthdays:
        header.append(f"@{i.id}:\t{i.content}")
    if doc.media:
        header.append(f"@Media:\t{doc.media.name}, {doc.media.type.value}")

    return "\n".join(header)

