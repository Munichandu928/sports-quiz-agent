"""
Seed sports knowledge base for ChromaDB.
This gives the RAG pipeline a base layer of factual sports knowledge
(history, records, tournaments, rules) that is combined at query time
with fresh web search results, so the agent isn't purely reliant on
live search for well-established facts.

In a production system this would be populated from a much larger
curated dataset / scraped sports encyclopedia. For this assignment it
is a representative seed set covering the sports in the brief.
"""

SPORTS_KNOWLEDGE = {
    "Cricket": [
        "India won the ICC Cricket World Cup in 1983, 2011, and 2024 (T20 World Cup).",
        "Sachin Tendulkar holds the record for most runs in Test cricket history, with over 15,000 runs.",
        "The longest format of cricket is Test cricket, played over five days.",
        "Australia has won the most Cricket World Cups, with six titles as of 2023.",
        "A standard T20 cricket match consists of 20 overs per side.",
        "The 'Ashes' is a Test cricket series played between England and Australia.",
        "Muttiah Muralitharan holds the record for most wickets taken in both Test and ODI cricket.",
        "The Indian Premier League (IPL) is the most-watched domestic T20 cricket league in the world.",
        "A century in cricket refers to a batsman scoring 100 or more runs in a single innings.",
        "The 2023 ODI Cricket World Cup was hosted by India, with Australia winning the final against India.",
    ],
    "Football": [
        "Lionel Messi and Cristiano Ronaldo are widely regarded as two of the greatest footballers of all time.",
        "The FIFA World Cup is held every four years; Brazil has won it a record five times.",
        "Argentina won the FIFA World Cup in 2022, defeating France in the final on penalties.",
        "A standard football (soccer) match consists of two 45-minute halves.",
        "The English Premier League is one of the most-watched football leagues globally.",
        "Lionel Messi won a record eight Ballon d'Or awards as of 2023.",
        "The offside rule is one of the most debated laws in football.",
        "Real Madrid has won the UEFA Champions League a record 15 times as of 2024.",
        "The 2026 FIFA World Cup will be co-hosted by the United States, Canada, and Mexico.",
        "Pele is the only footballer to win three FIFA World Cups (1958, 1962, 1970).",
    ],
    "Tennis": [
        "The four Grand Slam tournaments are the Australian Open, French Open, Wimbledon, and the US Open.",
        "Novak Djokovic holds the record for most Grand Slam men's singles titles.",
        "Serena Williams won 23 Grand Slam singles titles, the most in the Open Era.",
        "Wimbledon is the oldest tennis tournament in the world, first held in 1877.",
        "A tennis match is won by winning the majority of sets, typically best of three or best of five for men's Grand Slams.",
        "The French Open is the only Grand Slam played on clay courts.",
        "Rafael Nadal is nicknamed the 'King of Clay' due to his dominance at the French Open.",
        "Roger Federer won a record eight Wimbledon men's singles titles.",
        "A 'love' in tennis scoring means a score of zero.",
        "The Davis Cup is the premier international team competition in men's tennis.",
    ],
    "Badminton": [
        "India won its first-ever Thomas Cup title in 2022, defeating Indonesia in the final.",
        "The Thomas Cup is the premier men's team badminton championship, held every two years.",
        "The Uber Cup is the women's equivalent of the Thomas Cup.",
        "PV Sindhu became the first Indian woman to win an Olympic silver medal in badminton, at Rio 2016.",
        "Badminton is one of the fastest racquet sports; smash speeds have exceeded 400 km/h.",
        "China has traditionally been one of the most dominant nations in international badminton.",
        "The BWF (Badminton World Federation) governs international badminton competitions.",
        "A standard badminton match is best of three games, each played to 21 points.",
        "Lin Dan is regarded as one of the greatest badminton players in history, with two Olympic gold medals.",
        "Saina Nehwal won a bronze medal in badminton at the London 2012 Olympics.",
    ],
    "Basketball": [
        "The NBA (National Basketball Association) is the premier professional basketball league in the world.",
        "Kareem Abdul-Jabbar was the NBA's all-time leading scorer until Lebron James surpassed him in 2023.",
        "Michael Jordan won six NBA championships with the Chicago Bulls in the 1990s.",
        "A standard NBA basketball game consists of four 12-minute quarters.",
        "The FIBA Basketball World Cup is the premier international men's basketball tournament.",
        "The United States has won the most Olympic gold medals in men's basketball.",
        "Lebron James became the NBA's all-time leading scorer in February 2023.",
        "A three-point shot in basketball is worth three points and must be taken from beyond the arc.",
        "The Boston Celtics and Los Angeles Lakers have won the most NBA championships in history.",
        "Stephen Curry is widely credited with revolutionizing the game with his three-point shooting.",
    ],
}
