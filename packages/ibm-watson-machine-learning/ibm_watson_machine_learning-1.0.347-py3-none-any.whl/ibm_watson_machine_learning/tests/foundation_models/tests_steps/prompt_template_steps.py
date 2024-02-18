#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023-2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

from ibm_watson_machine_learning.foundation_models.prompts import PromptTemplate
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes


class PromptTemplateSteps:
    def __init__(self, data_storage):
        self.data_storage = data_storage

    check_value_error_message = "ERROR: Value it is NOT the same!"
    prompt_list_is_empty_message = "INFO: Prompt list is empty!"
    update_error_message = "ERROR: Name it is not updated!"
    nothing_to_unlock_message = "INFO: There is not any prompt to unlock!"
    lock_changed_error_message = "ERROR: Lock did not changed!"
    nothing_to_lock_message = "INFO: There is not any prompt to unlock!"
    prompt_list_is_not_empty_error_message = "ERROR: list it is not empty"
    lock_state_error_message = "ERROR: Cannot get lock state of prompts!"
    prompt_name = "Testing Prompt - TG"

    def create_prompt(self, prompt_mgr):
        instruction = "Write a summary"
        input_prefix = "Text"
        output_prefix = "Summary"
        input_text = "Bob has a dog"
        examples = [["Text1", "Summary1"]]

        prompt_template = PromptTemplate(name=self.prompt_name,
                                         model_id=ModelTypes.FLAN_UL2,
                                         input_text=input_text,
                                         instruction=instruction,
                                         input_prefix=input_prefix,
                                         output_prefix=output_prefix,
                                         examples=examples)

        prompt_mgr.store_prompt(prompt_template)

        assert prompt_template.name == self.prompt_name, self.check_value_error_message
        assert prompt_template.instruction == instruction, self.check_value_error_message
        assert prompt_template.input_prefix == input_prefix, self.check_value_error_message
        assert prompt_template.input_text == input_text, self.check_value_error_message
        assert prompt_template.output_prefix == output_prefix, self.check_value_error_message
        assert prompt_template.examples == examples, self.check_value_error_message

    def get_prompts_list(self, prompt_mgr):
        prompt_list = prompt_mgr.list()['ID']
        
        if len(prompt_list) == 0:
            raise Exception(self.prompt_list_is_empty_message)
        
        return prompt_list

    def find_existing_prompt(self, prompt_mgr, position):
        prompt_list = prompt_mgr.list()['ID']
        first_existing_prompt = prompt_mgr.list()['ID'][position]

        assert prompt_list.eq(first_existing_prompt).any(), self.prompt_list_is_empty_message

        return first_existing_prompt

    def edit_existing_prompt(self, prompt_mgr, first_id_element):
        new_name = "New Test Template Name - TG"
        new_instruction = "Updated Write a summary"
        new_input_prefix = "Updated Text"
        new_output_prefix = "Updated Summary"
        new_input_text = "Updated Input Text"
        new_examples = [["Updated Text - 1", "Updated Summary - 1"],
                        ["Updated Text - 2", "Updated Summary - 2"]]

        loaded_old_prompt = prompt_mgr.load_prompt(first_id_element)
        loaded_old_prompt.name = new_name
        loaded_old_prompt.instruction = new_instruction
        loaded_old_prompt.input_prefix = new_input_prefix
        loaded_old_prompt.output_prefix = new_output_prefix
        loaded_old_prompt.input_text = new_input_text
        loaded_old_prompt.examples = new_examples

        prompt_mgr.update_prompt(first_id_element, loaded_old_prompt)

        loaded_updated_prompt = prompt_mgr.load_prompt(first_id_element)

        assert loaded_updated_prompt.name == new_name, self.update_error_message
        assert loaded_updated_prompt.instruction == new_instruction, self.update_error_message
        assert loaded_updated_prompt.input_prefix == new_input_prefix, self.update_error_message
        assert loaded_updated_prompt.output_prefix == new_output_prefix, self.update_error_message
        assert loaded_updated_prompt.input_text == new_input_text, self.update_error_message
        assert loaded_updated_prompt.examples == new_examples, self.update_error_message

    def unlock_prompt(self, prompt_mgr, prompt_id):
        prompt_mgr.unlock(prompt_id)
        lock_state = prompt_mgr.get_lock(prompt_id)

        assert not lock_state["locked"], self.lock_changed_error_message

    def lock_prompt(self, prompt_mgr, prompt_id):
        prompt_mgr.lock(prompt_id)
        lock_state = prompt_mgr.get_lock(prompt_id)

        assert lock_state["locked"], self.lock_changed_error_message

    def get_lock_state(self, prompt_mgr, prompt_id):
        lock_state = prompt_mgr.get_lock(prompt_id)

        assert True or False in lock_state, self.lock_state_error_message
        return lock_state

    def load_prompt(self, prompt_mgr, prompt_id):
        loaded_prompt = prompt_mgr.load_prompt(prompt_id)

        return loaded_prompt

    def create_freeform_prompt(self, prompt_mgr):
        input_text = "Bob has a {object}"

        prompt_template = PromptTemplate(name=self.prompt_name,
                                         input_text=input_text,
                                         input_variables=["object"],
                                         model_id=ModelTypes.FLAN_UL2)

        prompt_mgr.store_prompt(prompt_template)

        assert prompt_template.name == self.prompt_name, self.check_value_error_message
        assert prompt_template.input_text == input_text, self.check_value_error_message

    def delete_prompt_template(self, prompt_mgr, prompt_id):
        prompt_mgr.delete_prompt(prompt_id, force=True)

        assert prompt_id not in prompt_mgr.list()['ID']
