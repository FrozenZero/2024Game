"""
@Author  ：dlfrozen
@Date    ：2024/1/6 12:14
获取文章的段落，返回列表

"""

import requests
from urllib.parse import urlsplit
import json

cookies = {
    'g_state': '{"i_l":1,"i_p":1704462537746}',
    '_gid': 'GA1.2.1577861696.1704457689',
    'lightstep_guid/medium-web': 'bff4aec4286ef804',
    'lightstep_session_id': '2fb2c3709e06db33',
    'sz': '1695',
    'pr': '1.5',
    'tz': '-480',
    'nonce': 'syWcspAD',
    'xsrf': 'Drz6WHda1hVEVKnZ',
    'uid': 'ad27f7f92362',
    'sid': '1:Hlpi9gjpN7pM8u9zJnUT8EITEm0Td2ImA0pLZkXTkTtGjU3myqdYK8jtbKkHlFx1',
    '_ga': 'GA1.1.1071984854.1701310103',
    '_ga_7JY7T788PK': 'GS1.1.1704509245.8.1.1704509286.0.0.0',
    '_dd_s': 'rum=0&expire=1704510186990',
    'dd_cookie_test_c7433118-ccfd-4a1d-917b-79a50f84385d': 'test',
}


def gen_headers(url):
    medium_frontend_path = urlsplit(url).path
    headers = {
        'authority': 'medium.com',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'apollographql-client-name': 'lite',
        'apollographql-client-version': 'main-20240105-172446-fe9cfbd9ba',
        'content-type': 'application/json',
        'cookie': 'g_state={"i_l":1,"i_p":1704462537746}; lightstep_guid/medium-web=bff4aec4286ef804; lightstep_session_id=2fb2c3709e06db33; sz=1695; pr=1.5; tz=-480; nonce=syWcspAD; uid=ad27f7f92362; sid=1:Hlpi9gjpN7pM8u9zJnUT8EITEm0Td2ImA0pLZkXTkTtGjU3myqdYK8jtbKkHlFx1; _ga=GA1.1.1071984854.1701310103; xsrf=dd4c2a2c8f51; _ga_7JY7T788PK=GS1.1.1704699806.12.0.1704699847.0.0.0; dd_cookie_test_1577947f-d532-458c-a643-047a1625f37f=test; _dd_s=rum=0&expire=1704700747390; dd_cookie_test_d69e4c7e-5971-4c0f-ba20-cbcb738b839c=test',
        'graphql-operation': 'WebInlineTopicFeedQuery',
        'medium-frontend-app': 'lite/main-20240105-172446-fe9cfbd9ba',
        'medium-frontend-path': medium_frontend_path,
        'medium-frontend-route': 'homepage',
        'origin': 'https://medium.com',
        'ot-tracer-sampled': 'true',
        'ot-tracer-spanid': '7441ee9736437634',
        'ot-tracer-traceid': '671194f95f854582',
        'referer': url,
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    return headers


def gen_json_data(url):
    id = url.split('-')[-1]
    json_data = [
        {
            'operationName': 'PostViewerEdgeContentQuery',
            'variables': {
                'postId': id,
                'postMeteringOptions': {
                    'referrer': '',
                },
            },
            'query': 'query PostViewerEdgeContentQuery($postId: ID!, $postMeteringOptions: PostMeteringOptions) {\n  post(id: $postId) {\n    ... on Post {\n      id\n      viewerEdge {\n        id\n        fullContent(postMeteringOptions: $postMeteringOptions) {\n          isLockedPreviewOnly\n          validatedShareKey\n          bodyModel {\n            ...PostBody_bodyModel\n            __typename\n          }\n          ...FriendLinkMeter_postContent\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment PostBody_bodyModel on RichText {\n  sections {\n    name\n    startIndex\n    textLayout\n    imageLayout\n    backgroundImage {\n      id\n      originalHeight\n      originalWidth\n      __typename\n    }\n    videoLayout\n    backgroundVideo {\n      videoId\n      originalHeight\n      originalWidth\n      previewImageId\n      __typename\n    }\n    __typename\n  }\n  paragraphs {\n    id\n    ...PostBodySection_paragraph\n    __typename\n  }\n  ...normalizedBodyModel_richText\n  __typename\n}\n\nfragment PostBodySection_paragraph on Paragraph {\n  name\n  ...PostBodyParagraph_paragraph\n  __typename\n  id\n}\n\nfragment PostBodyParagraph_paragraph on Paragraph {\n  name\n  type\n  ...ImageParagraph_paragraph\n  ...TextParagraph_paragraph\n  ...IframeParagraph_paragraph\n  ...MixtapeParagraph_paragraph\n  ...CodeBlockParagraph_paragraph\n  __typename\n  id\n}\n\nfragment ImageParagraph_paragraph on Paragraph {\n  href\n  layout\n  metadata {\n    id\n    originalHeight\n    originalWidth\n    focusPercentX\n    focusPercentY\n    alt\n    __typename\n  }\n  ...Markups_paragraph\n  ...ParagraphRefsMapContext_paragraph\n  ...PostAnnotationsMarker_paragraph\n  __typename\n  id\n}\n\nfragment Markups_paragraph on Paragraph {\n  name\n  text\n  hasDropCap\n  dropCapImage {\n    ...MarkupNode_data_dropCapImage\n    __typename\n    id\n  }\n  markups {\n    ...Markups_markup\n    __typename\n  }\n  __typename\n  id\n}\n\nfragment MarkupNode_data_dropCapImage on ImageMetadata {\n  ...DropCap_image\n  __typename\n  id\n}\n\nfragment DropCap_image on ImageMetadata {\n  id\n  originalHeight\n  originalWidth\n  __typename\n}\n\nfragment Markups_markup on Markup {\n  type\n  start\n  end\n  href\n  anchorType\n  userId\n  linkMetadata {\n    httpStatus\n    __typename\n  }\n  __typename\n}\n\nfragment ParagraphRefsMapContext_paragraph on Paragraph {\n  id\n  name\n  text\n  __typename\n}\n\nfragment PostAnnotationsMarker_paragraph on Paragraph {\n  ...PostViewNoteCard_paragraph\n  __typename\n  id\n}\n\nfragment PostViewNoteCard_paragraph on Paragraph {\n  name\n  __typename\n  id\n}\n\nfragment TextParagraph_paragraph on Paragraph {\n  type\n  hasDropCap\n  codeBlockMetadata {\n    mode\n    lang\n    __typename\n  }\n  ...Markups_paragraph\n  ...ParagraphRefsMapContext_paragraph\n  __typename\n  id\n}\n\nfragment IframeParagraph_paragraph on Paragraph {\n  type\n  iframe {\n    mediaResource {\n      id\n      iframeSrc\n      iframeHeight\n      iframeWidth\n      title\n      __typename\n    }\n    __typename\n  }\n  layout\n  ...Markups_paragraph\n  __typename\n  id\n}\n\nfragment MixtapeParagraph_paragraph on Paragraph {\n  type\n  mixtapeMetadata {\n    href\n    mediaResource {\n      mediumCatalog {\n        id\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  ...GenericMixtapeParagraph_paragraph\n  __typename\n  id\n}\n\nfragment GenericMixtapeParagraph_paragraph on Paragraph {\n  text\n  mixtapeMetadata {\n    href\n    thumbnailImageId\n    __typename\n  }\n  markups {\n    start\n    end\n    type\n    href\n    __typename\n  }\n  __typename\n  id\n}\n\nfragment CodeBlockParagraph_paragraph on Paragraph {\n  codeBlockMetadata {\n    lang\n    mode\n    __typename\n  }\n  __typename\n  id\n}\n\nfragment normalizedBodyModel_richText on RichText {\n  paragraphs {\n    ...normalizedBodyModel_richText_paragraphs\n    __typename\n  }\n  sections {\n    startIndex\n    ...getSectionEndIndex_section\n    __typename\n  }\n  ...getParagraphStyles_richText\n  ...getParagraphSpaces_richText\n  __typename\n}\n\nfragment normalizedBodyModel_richText_paragraphs on Paragraph {\n  markups {\n    ...normalizedBodyModel_richText_paragraphs_markups\n    __typename\n  }\n  codeBlockMetadata {\n    lang\n    mode\n    __typename\n  }\n  ...getParagraphHighlights_paragraph\n  ...getParagraphPrivateNotes_paragraph\n  __typename\n  id\n}\n\nfragment normalizedBodyModel_richText_paragraphs_markups on Markup {\n  type\n  __typename\n}\n\nfragment getParagraphHighlights_paragraph on Paragraph {\n  name\n  __typename\n  id\n}\n\nfragment getParagraphPrivateNotes_paragraph on Paragraph {\n  name\n  __typename\n  id\n}\n\nfragment getSectionEndIndex_section on Section {\n  startIndex\n  __typename\n}\n\nfragment getParagraphStyles_richText on RichText {\n  paragraphs {\n    text\n    type\n    __typename\n  }\n  sections {\n    ...getSectionEndIndex_section\n    __typename\n  }\n  __typename\n}\n\nfragment getParagraphSpaces_richText on RichText {\n  paragraphs {\n    layout\n    metadata {\n      originalHeight\n      originalWidth\n      id\n      __typename\n    }\n    type\n    ...paragraphExtendsImageGrid_paragraph\n    __typename\n  }\n  ...getSeriesParagraphTopSpacings_richText\n  ...getPostParagraphTopSpacings_richText\n  __typename\n}\n\nfragment paragraphExtendsImageGrid_paragraph on Paragraph {\n  layout\n  type\n  __typename\n  id\n}\n\nfragment getSeriesParagraphTopSpacings_richText on RichText {\n  paragraphs {\n    id\n    __typename\n  }\n  sections {\n    ...getSectionEndIndex_section\n    __typename\n  }\n  __typename\n}\n\nfragment getPostParagraphTopSpacings_richText on RichText {\n  paragraphs {\n    type\n    layout\n    text\n    codeBlockMetadata {\n      lang\n      mode\n      __typename\n    }\n    __typename\n  }\n  sections {\n    ...getSectionEndIndex_section\n    __typename\n  }\n  __typename\n}\n\nfragment FriendLinkMeter_postContent on PostContent {\n  validatedShareKey\n  shareKeyCreator {\n    ...FriendLinkSharer_user\n    __typename\n    id\n  }\n  __typename\n}\n\nfragment FriendLinkSharer_user on User {\n  id\n  name\n  ...userUrl_user\n  __typename\n}\n\nfragment userUrl_user on User {\n  __typename\n  id\n  customDomainState {\n    live {\n      domain\n      __typename\n    }\n    __typename\n  }\n  hasSubdomain\n  username\n}\n',
        },
    ]
    return json_data


# def get_article_paragraph(args):
#     article_name, url =args
#     # url ="https://andrewzuo.com/another-idiot-boldly-proclaims-that-they-cant-solve-a-basic-programming-problem-4bbdf4eeb86c"
#     response = requests.post('https://andrewzuo.com/_/graphql', cookies=cookies, headers=gen_headers(url),
#                              json=gen_json_data(url))
#     a_list = []
#     content = json.loads(response.text)
#     items = content[0].get('data').get('post').get('viewerEdge').get('fullContent').get('bodyModel').get("paragraphs")
#
#     for item in items:
#         text = item.get('text')
#         type = item.get('type')  # H3 H4 P IMG
#         if type not in ("H3", "H4", "P"):
#             continue
#         a_list.append([text, type])
#     return [article_name,a_list]

def get_article_paragraph(args):
    article_name, url =args
    # url ="https://andrewzuo.com/another-idiot-boldly-proclaims-that-they-cant-solve-a-basic-programming-problem-4bbdf4eeb86c"
    response = requests.post('https://andrewzuo.com/_/graphql', cookies=cookies, headers=gen_headers(url),
                             json=gen_json_data(url))
    a_list = []
    content = json.loads(response.text)
    items = content[0].get('data').get('post').get('viewerEdge').get('fullContent').get('bodyModel').get("paragraphs")

    for item in items:
        text = item.get('text')
        type = item.get('type')  # H3 H4 P IMG
        if type not in ("H3", "H4", "P"):
            continue
        a_list.append([text, type])
    return [article_name,a_list]

def get_article_paragraphs(pool,args,result_queue):
     async_results = pool.map_async(get_article_paragraph, args, callback=result_queue.put)
     return async_results
