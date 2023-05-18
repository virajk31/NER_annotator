from st_text_annotator import StTextAnnotator
import streamlit as st
import json


st.header("Dataset annotation")
st.subheader("Do not Click Add")


uploaded_file = st.file_uploader("Upload a file", type="json")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    # with open(bytes_data) as f:
    data = json.loads(bytes_data)
    text = [t['drug_name'] for t in data]

    # Initialize session state
    state = st.session_state

    col1, col2 = st.columns([1,1])
    # Navigation buttons
    with col1:
        if st.button('Next') and state.current_index < len(state.files) - 1:
            state.current_index += 1
    with col2:
        if st.button('Previous') and state.current_index > 0:
            state.current_index -= 1


    if "annotations" not in state:
        state.annotations = {}
        state.files = text
        state.current_index = 0  # use an index instead of the text itself


    # Display current file
    current_file = state.files[state.current_index]
    # st.write(f'Annotating drug: {current_file}')

    annotation = StTextAnnotator(current_file)

    st.write(annotation)


    # # Load annotation if it exists, else create new annotation
    # if current_file in state.annotations:
    #     annotation = state.annotations[current_file]
    # else:
    #     annotation = StTextAnnotator(current_file)

    print('annotation',annotation)

    # Display annotation tool
    state.annotations[current_file] = annotation

    # # Display all annotations
    # if st.button('Show all annotations'):
    #     st.write(state.annotations)
    with st.sidebar:
        # st.write("This code will be printed to the sidebar.")
        st.write(state.annotations)
        
            
    # Save annotations to json file

    import pickle
    TRAIN_DATA = []

    for text, annotations in state.annotations.items():
        entities = []
        for annotation in annotations:
            for entity in annotation:
                start = entity["start"]
                end = entity["end"]
                label = entity["label"]
                entities.append((start, end, 'DRUG',label))  # Convert list to tuple
        if entities != []:            
            TRAIN_DATA.append((text, {"entities": entities}))  # Convert list to tuple

    print('TRAIN_DATA',TRAIN_DATA)
    if st.button('Save annotations'):
        with open('train_data.pkl', 'wb') as pkl_file:
            pickle.dump(TRAIN_DATA, pkl_file)
        st.success("Annotations saved to train_data.pkl")


