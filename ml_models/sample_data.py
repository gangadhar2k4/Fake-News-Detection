import pandas as pd
import numpy as np


def get_sample_data():
    """
    Generate sample training data for the fake news detection models.
    In a real application, this would load from a proper dataset.
    """
    
    # Sample real news articles
    real_news = [
        "Scientists at MIT have successfully developed a new method for producing clean energy using advanced solar panel technology that could revolutionize renewable energy production worldwide.",
        "The World Health Organization announced new guidelines for preventing the spread of infectious diseases in healthcare facilities, emphasizing the importance of proper sanitation protocols.",
        "NASA's latest Mars rover has discovered evidence of ancient water flows on the planet's surface, providing new insights into the possibility of past life on Mars.",
        "A breakthrough study published in Nature reveals that certain dietary changes can significantly reduce the risk of cardiovascular disease in adults over 50.",
        "The Federal Reserve announced a modest increase in interest rates to combat inflation while maintaining economic stability and supporting job growth.",
        "Researchers at Stanford University have developed a new artificial intelligence system that can accurately predict earthquake occurrences with 85% accuracy.",
        "The United Nations Climate Summit concluded with 195 countries agreeing to new carbon emission reduction targets aimed at limiting global temperature rise.",
        "A new study from Harvard Medical School shows that regular exercise can improve cognitive function and reduce the risk of dementia in older adults.",
        "Tech companies are investing billions in quantum computing research, with IBM announcing a breakthrough in quantum error correction that could accelerate practical applications.",
        "The European Space Agency successfully launched its latest Earth observation satellite to monitor climate change and environmental conditions globally.",
        "Medical researchers have identified a new biomarker that could lead to earlier detection of Alzheimer's disease, potentially improving treatment outcomes.",
        "The International Monetary Fund projects steady global economic growth for the next fiscal year, citing improved trade relations and technological advancement.",
        "A collaborative study between universities shows that renewable energy sources now account for 30% of global electricity generation, marking a significant milestone.",
        "The Food and Drug Administration approved a new vaccine that shows 95% effectiveness against a strain of influenza that has been particularly challenging to treat.",
        "Urban planners are implementing smart city technologies in major metropolitan areas to improve traffic flow, reduce pollution, and enhance quality of life for residents."
    ]
    
    # Sample fake news articles
    fake_news = [
        "Local man discovers that drinking lemon water for 30 days cures all forms of cancer and doctors don't want you to know this simple trick.",
        "Breaking: Government officials confirm that aliens have been living among us for decades and are planning to reveal themselves next month.",
        "Shocking study reveals that vaccines contain microchips designed to control human behavior and track every movement of the population.",
        "Scientists discover that the Earth is actually flat and NASA has been covering up this truth for over 50 years using fake satellite images.",
        "Miracle weight loss pill allows people to lose 50 pounds in one week without any diet or exercise, doctors hate this one simple trick.",
        "Breaking news: All smartphones secretly record conversations 24/7 and sell the data to foreign governments for mind control experiments.",
        "Local grandmother's homemade remedy using common kitchen ingredients completely eliminates diabetes and Big Pharma is trying to suppress this information.",
        "Exclusive: Time traveler from 2050 warns that the world will end in 2030 unless we stop using the internet immediately.",
        "Secret government documents reveal that weather is completely controlled by machines and natural weather patterns no longer exist anywhere on Earth.",
        "Health experts discover that drinking bleach mixed with orange juice can cure any viral infection within hours, pharmaceutical companies are furious.",
        "Leaked footage shows that all major news events are staged with actors and nothing reported on television or newspapers is actually real.",
        "Revolutionary discovery: Crystals placed under your pillow can cure mental illness and improve IQ by 100 points within just two weeks.",
        "Underground scientists prove that gravity is just a hoax and objects fall down because of invisible magnetic forces controlled by secret societies.",
        "Exclusive investigation reveals that all birds are actually government drones designed to spy on citizens and real birds went extinct in 1986.",
        "Ancient text discovered in remote cave shows that humans can live forever by following this one weird diet that includes only raw vegetables and moonlight."
    ]
    
    # Create DataFrame
    data = []
    
    # Add real news samples
    for article in real_news:
        data.append({
            'text': article,
            'label': 'Real'
        })
    
    # Add fake news samples
    for article in fake_news:
        data.append({
            'text': article,
            'label': 'Fake'
        })
    
    # Add some mixed/partially true samples
    partially_true = [
        "A study suggests that coffee may have health benefits, but the research was conducted on a small sample size and results may not be generalizable.",
        "Local politician claims to have reduced crime rates by 50%, though independent fact-checkers note that the decrease aligns with national trends.",
        "New technology promises to improve internet speeds significantly, but early users report mixed results and some technical difficulties.",
        "Health officials recommend a new treatment that shows promise in clinical trials, though long-term effects are still being studied.",
        "Company announces record profits for the quarter, but financial analysts note that the growth is primarily due to one-time asset sales rather than core business performance."
    ]
    
    for article in partially_true:
        data.append({
            'text': article,
            'label': 'Real'  # Treating partially true as real for binary classification
        })
    
    # Create and shuffle DataFrame
    df = pd.DataFrame(data)
    df = df.sample(frac=1).reset_index(drop=True)  # Shuffle the data
    
    return df


def get_additional_training_data():
    """
    Additional training samples for better model performance.
    This expands the dataset with more diverse examples.
    """
    
    additional_real = [
        "The stock market experienced moderate gains today following positive earnings reports from major technology companies and improved economic indicators.",
        "Researchers at Johns Hopkins University published findings showing the effectiveness of a new treatment protocol for patients with chronic conditions.",
        "The Department of Education announced new funding initiatives to support STEM education programs in underserved communities across the nation.",
        "Environmental scientists report that conservation efforts have led to a 15% increase in endangered species populations over the past five years.",
        "The International Olympic Committee confirmed the dates and venues for the upcoming games, with enhanced safety protocols due to ongoing health concerns."
    ]
    
    additional_fake = [
        "Doctors are amazed by this one weird trick that eliminates wrinkles overnight using only items found in your kitchen pantry.",
        "Secret society of billionaires controls the weather using hidden machines located in underground bunkers around the world.",
        "Local man wins lottery 47 times using this simple mathematical formula that lottery officials don't want you to discover.",
        "Breaking: Scientists confirm that wearing aluminum foil hats actually protects against government mind reading technology.",
        "Miracle plant found in remote jungle cures every known disease and pharmaceutical companies are desperately trying to hide its existence."
    ]
    
    data = []
    
    for article in additional_real:
        data.append({'text': article, 'label': 'Real'})
    
    for article in additional_fake:
        data.append({'text': article, 'label': 'Fake'})
    
    return pd.DataFrame(data)


if __name__ == "__main__":
    # Test the data generation
    sample_data = get_sample_data()
    print(f"Generated {len(sample_data)} training samples")
    print(f"Real news samples: {len(sample_data[sample_data['label'] == 'Real'])}")
    print(f"Fake news samples: {len(sample_data[sample_data['label'] == 'Fake'])}")
    print("\nSample entries:")
    print(sample_data.head())
