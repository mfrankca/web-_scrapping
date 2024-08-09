import EbayScraper
import streamlit as st

averagePrice = EbayScraper.Average(query='Bolle Parole / Vigilante Sunglasses Temple Tips Matte Black Set x 2', condition='new')
st.write(averagePrice)

itemList = EbayScraper.Items(query='FLEXON 472 023 Silver Lilac Eyeglasses 472-023 50mm Marchon', country='us', condition='new')
st.write(itemList[0])

#"https://www.ebay.com/itm/296138589257?hash=item44f33c4449%3Ag%3As54AAOSwMRNlkWfk&itmprp=enc%3AAQAJAAABACHAbcnHkcCH0cMnoz5DyMuk%2F2S006oab039Ydiz4BBkh%2B82ebGvZwLxrhL4UfTmoOc%2B91Fl%2BZ27I1NLFzR7Rs%2FZZlRMOut1tmggbKVBQPrcZFA4YNuynxoi3QYA95x9OraC9YGTv6puZ6CRuYykaFbhxaIlRCrf0X3ipE3MLZgfORukd3%2BhZdFYgIkwIIkskMmiMnpa5ByhE%2FJZpfjruh0nzkNV2firmopAEq0VZ5lJgTVr457FtkaEXnoXhp%2FnJlEpt8mgQol12Bek5D47zvnhdoxJbF%2BKVWPpE4p2QqZMtXZVKaoMHu%2Bz1dJWXcwifWEH8ckj0GT2dbF0%2F9wqFtM%3D%7Ctkp%3ABk9SR8LCpc-mZA&LH_Ite"