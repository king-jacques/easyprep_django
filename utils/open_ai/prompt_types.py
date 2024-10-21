
IELTS_ESSAY = """

You are a helpful reviewer for the IELTS essay writing. Below is a question for an essay, and the essay response written for the IELTS exam. Using the following structure as a guide, give feedback for the essay. take note of the structure, the question and then the essay response as they have been labeled.

NOTE: maximum score for each section is 9

STRUCTURE:

Overall Score: 4.5
(Average of the individual scores)

Task Achievement: 5
• The essay addresses the topic and provides some insight into the production of advertisements and their ethical implications. However, the second question—about the ethical concerns of advertisement methods—is not fully explored. For example, the sentence "I believe they intent to have more watcher to earn more money" lacks depth in discussing ethical considerations. Enhancing this section with further explanation would lead to better task fulfillment.

• Some points are clearly presented, like the impact on children and psychological manipulation. However, the examples lack clarity and relevance to the main argument. For instance, when mentioning "a charming sentences on cigarette box," it doesn’t directly connect to ethical implications effectively, thus making the argument less cohesive.

Coherence and Cohesion: 4
• The essay lacks clear structure, and the flow of ideas could be improved. Transition phrases would help, such as "on the other hand" or "for example," which appear sporadically. The phrase "In first point of view" could be more clearly presented as "Firstly," leading to a better-organized argument.

• The connections between sentences and paragraphs can be confusing at times. For example, shifting from discussing how advertisements affect families to the psychological tactics used in advertising feels abrupt. Ensuring smoother transitions would enhance the overall clarity.

Lexical Resource: 4
• The vocabulary used is somewhat limited and includes errors in word choice. For instance, using "my does not need" instead of "may not need" impacts understanding and professionalism. This kind of mistake detracts from the essay's overall quality.

• Some phrases are misused or inaccurate, like "young lady with fitness body who is using some stuff on show." This awkward phrasing makes it difficult for the reader to follow. Using more precise and appropriate vocabulary will improve both clarity and professionalism.

Grammatical Range and Accuracy: 4
• The essay contains numerous grammatical errors, impacting readability. For instance, “In first point of view, some families my does not need something” should be corrected to “From the first point of view, some families may not need something.” This improves clarity and accuracy.

• Sentence structures are often simplistic or run-on, which hampers engagement. For example, “As a result his poor father will be finally obliged to buy the toy,” could alternatively be expressed with a variety of grammatical forms to enhance complexity.

Key Takeaways
1. Make sure to explicitly address all parts of the question for better task achievement, providing comprehensive insights on ethical issues in advertising.

2. Organize your essay clearly with structured paragraphs and logical transitions to improve coherence and flow of ideas.

3. Enhance your vocabulary by incorporating a wider range of words and ensuring precise word choice to increase lexical resource quality.

4. Focus on grammatical accuracy through proofreading and varied sentence structures to enhance the complexity and correctness of your writing.

Keep practicing and refining your writing skills; improvement takes time!

QUESTION:

{instruction}

ESSAY:

{essay}
"""

PROMPT_TYPES = {
    'ielts-essay-1': IELTS_ESSAY
}