#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023-2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------


def test_create_prompt(prompt_template_step, prompt_mgr):
    prompt_template_step.create_prompt(prompt_mgr)


def test_create_freeform_prompt(prompt_template_step, prompt_mgr):
    prompt_template_step.create_freeform_prompt(prompt_mgr)


def test_update_prompt(prompt_template_step, prompt_mgr, prompt_template):
    first_id_element = prompt_template_step.find_existing_prompt(prompt_mgr, 0)
    prompt_template_step.edit_existing_prompt(prompt_mgr, first_id_element)


def test_unlock_prompts(prompt_template_step, prompt_mgr, prompt_template):
    prompt_list = prompt_template_step.get_prompts_list(prompt_mgr)
    position = 0

    for _ in range(len(prompt_list)):
        prompt = prompt_template_step.find_existing_prompt(prompt_mgr, position)
        lock_state = prompt_mgr.get_lock(prompt)

        if lock_state["locked"]:
            prompt_template_step.unlock_prompt(prompt_mgr, prompt)
            print(f'\nUnlocked - Prompt with ID:{prompt}!')
        else:
            print(f'\nPrompt with ID:{prompt} already unlocked!')

        position += 1


def test_lock_prompts(prompt_template_step, prompt_mgr, prompt_template):
    position = 0
    prompt_list = prompt_template_step.get_prompts_list(prompt_mgr)

    for _ in range(len(prompt_list)):
        prompt = prompt_template_step.find_existing_prompt(prompt_mgr, position)
        lock_state = prompt_mgr.get_lock(prompt)

        if not lock_state["locked"]:
            prompt_template_step.lock_prompt(prompt_mgr, prompt)
            print(f'\nLocked - Prompt with ID:{prompt}!')
        else:
            print(f'\nPrompt with ID:{prompt} already locked!')
        position += 1


def test_show_lock_state(prompt_template_step, prompt_mgr, prompt_template):
    position = 0
    prompt_list = prompt_template_step.get_prompts_list(prompt_mgr)

    for _ in range(len(prompt_list)):
        prompt = prompt_template_step.find_existing_prompt(prompt_mgr, position)
        state_list = prompt_template_step.get_lock_state(prompt_mgr, prompt)
        print(state_list)
        position += 1


def test_delete_prompt(prompt_template_step, prompt_mgr):
    position = 0
    prompt_list = prompt_template_step.get_prompts_list(prompt_mgr)

    for _ in range(len(prompt_list)):
        if len(prompt_list) > 0:
            prompt = prompt_template_step.find_existing_prompt(prompt_mgr, position)
            prompt_template_step.delete_prompt_template(prompt_mgr, prompt)
            print("\nPrompt: " + prompt + ": has been deleted")
