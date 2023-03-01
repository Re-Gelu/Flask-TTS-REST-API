import { API_SERVER } from './config.js';
import React from 'react';
import { useFormik } from 'formik';
 import * as Yup from 'yup';
import { useState, useEffect } from "react";
import UIkit from 'uikit';

/* Error API handler */
const error_handler = (response) => {
	const error_text = document.querySelector('#APIerror');
    if (response.message) {error_text.innerHTML = JSON.stringify(response.message)};
    if (response.task_result) {error_text.innerHTML = response.task_result};
    if (response.error) {error_text.innerHTML = response.error};
}

/* Upload event handler */
const event_handler = (data) => {

    /* Place spinner while waiting */
	document.querySelector('#downloadResultLink').innerHTML = '<div class="spinner-border" role="status"><span class="visually-hidden">Идёт обработка...</span></div>';

    /* Get task info every 1 sec  */
	const task_interval_id = setInterval(() => {
		fetch(`${API_SERVER}/tts/${data.task_id}`)
		.then(response => response.json())
		.then(
			response => {
				console.log(response);
				if (response.is_ready) {
                    if (response.task_result_url && response.is_successful) {
                        clearInterval(task_interval_id)
                        document.querySelector('#downloadResultLink').innerHTML = "Скачать результат!";
                        document.querySelector('#downloadResultLink').setAttribute('href', response.task_result_url);
                    }
                    else {error_handler(response);}
                }
			}
		)
		.catch(error => console.log(error.message));
	}, 1000);

};

/* Submit button event handler */
const onSubmit = (data) => {
	fetch(`${API_SERVER}/tts`, {
		method: 'POST',
		headers: {"Content-Type": "application/json" },
		body: JSON.stringify(data)
	})
	.then(response => response.json())
	.then(
		response => {
			if (!("error" in response)) {
				document.querySelector('#APIerror').innerHTML = '';
				event_handler(response);
			} else {
				document.querySelector('#downloadResultLink').innerHTML = '';
				error_handler(response);
			}
		}
	)
	.catch(error => console.log(error.message));
};

const TTSForm = (props) => {
	const formik = useFormik({
		initialValues: {
			text: "",
			voice_rate: parseInt(props.voiceRate),
			voice_volume: parseFloat(props.voiceVolume),
			voice_id: 0,
			use_AI: false,
			file: ""
		},
		validationSchema: Yup.object({
			text: Yup.string()
				.min(1, 'No text provided!')
				.max(10000, 'Must be 10000 characters or less'),
			voice_rate: Yup.number()
				.min(props.minVoiceRate)
				.max(props.maxVoiceRate)
				.required(),
			voice_volume: Yup.number()
				.min(props.minVoiceVolume)
				.max(props.maxVoiceVolume)
				.required(),
			voice_id: Yup.number()
				.min(0)
				.required(),
			use_AI: Yup.bool()
				.oneOf([true, false])
				.required(),
		}),
		onSubmit: values => {
			onSubmit(values);
		}
	});

	const [isVoicesLoaded, setVoicesIsLoaded] = useState(false);
	const [voicesList, setVoicesList] = useState({});

	useEffect(() => {
		fetch(`${API_SERVER}/tts`)
		.then(response => response.json())
		.then(
			response => {
				setVoicesIsLoaded(true);
				setVoicesList(response);
			},
			error => {
				setVoicesIsLoaded(false);
				console.log(error);
			}
		)
		.catch(error => console.log(error.message));

		const bar =  document.querySelector('#js-progressbar');

		UIkit.upload('.js-upload', {

			method: "POST",
			url: `${API_SERVER}/tts`,
			multiple: false,
			name: "file",

			beforeSend: function (environment) {
				environment.data.set('voice_rate', document.querySelector('#voiceRateRange').value);
				environment.data.set('voice_id', document.querySelector('#voiceSelect').value);
				environment.data.set('voice_volume', document.querySelector('#voiceVolumeRange').value);
			},

			loadStart: function (e) {
				document.querySelector('#APIerror').innerHTML = '';
				bar.removeAttribute('hidden');
				bar.max = e.total;
				bar.value = e.loaded;
			},

			progress: function (e) {
				bar.max = e.total;
				bar.value = e.loaded;
			},

			loadEnd: function (e) {
				bar.max = e.total;
				bar.value = e.loaded;
			},

			complete: function (e) {
				setTimeout(function () {
					bar.setAttribute('hidden', 'hidden');
				}, 500);
				event_handler(JSON.parse(e.responseText));
			},

			error: function () {
				setTimeout(function () {
					bar.setAttribute('hidden', 'hidden');
				}, 500);
				const response = JSON.parse(arguments[0].xhr.responseText);
				error_handler(response);
			},
		});
	}, []);

	return (
		<form className="my-3" id="uploadForm" onSubmit={formik.handleSubmit}>
			<div className="row">

				<div className="col-md-4 col-12 my-3 my-md-0 uk-box-shadow-hover-medium">
					<input className="uk-range" type="range" {...formik.getFieldProps('voice_rate')} min={props.minVoiceRate} max={props.maxVoiceRate} step={props.voiceRateStep} uk-tooltip={props.voiceRateTooltip} id="voiceRateRange" name="voice_rate" />
				</div>

				<div className="col-md-4 col-12 my-3 my-md-0" id="voiceSelectRoot">
					<select className="form-select form-select-sm uk-box-shadow-hover-medium" {...formik.getFieldProps('voice_id')} uk-tooltip={props.voiceIdTooltip} id="voiceSelect" name="voice_id">
						{
							isVoicesLoaded ? 
								voicesList.voices.map( (item , key) => <option key={key} value={key}>{item.name}</option>)
							:
								<option key="0" value="0">Загрузка...</option>
						}
					</select>
				</div>

				<div className="col-md-4 col-12 my-3 my-md-0 uk-box-shadow-hover-medium">
					<input className="uk-range" type="range" {...formik.getFieldProps('voice_volume')} min={props.minVoiceVolume} max={props.maxVoiceVolume} step={props.voiceVolumeStep} uk-tooltip={props.voiceVolumeTooltip} id="voiceVolumeRange" name="voice_volume"/>
				</div>

			</div>

			<div className="my-0 my-md-2 d-inline-block uk-box-shadow-hover-medium p-2">
				<input className="uk-checkbox" type="checkbox" id="useAiCheckbox" name="use_AI" {...formik.getFieldProps('use_AI')} uk-tooltip={props.useAITooltip} />
				<label className="ms-2">Использовать нейросеть?</label>
			</div>
			
			<div className="my-md-0 my-3">
				<label htmlFor="text" className="form-label">Введите текст или прикрепите файл: </label>
				<textarea {...formik.getFieldProps('text')} className={"uk-textarea rounded uk-box-shadow-hover-medium " + (formik.errors.text ? "uk-form-danger is-invalid" : "")} id="text" rows={props.textareaRows} name="text"></textarea>
				{formik.errors.text ? <div className='invalid-feedback'>{formik.errors.text}</div> : null}
			</div>

			<div className="js-upload uk-placeholder uk-text-center rounded uk-box-shadow-hover-medium uk-drag">
				<i className="bi bi-file-earmark-arrow-up me-1"></i>
				<span className="uk-text-middle">Приложите файл, опустив его здесь или </span>
				<div uk-form-custom="true">
					<span className="text-colored">здесь</span>
					<input type="file" id="file" name="file" {...formik.getFieldProps('file')} />
				</div>
			</div>
							
			<progress id="js-progressbar" className="uk-progress" value="0" max="100" hidden></progress>

			<div id="APIerror" className="text-danger text-center mb-md-0 mb-3"></div>

			<div className="d-inline-flex align-items-center mt-md-3 mt-0" id="submitFormRow">
				<button  
					className="btn uk-button-text px-5 border-colored uk-box-shadow-hover-medium"
					type="submit">
					Отправить
				</button>
				<a id="downloadResultLink" className="mx-4 my-auto" download="true"></a>
			</div>
		</form>
	)
}


function App() {
  return
};

TTSForm.defaultProps = {
	textareaRows: "7",

	voiceRate: "200", 
	maxVoiceRate: "1000",
	minVoiceRate: "0",
	voiceRateStep: "10",
	voiceRateTooltip : "Скорость речи",

	voiceVolume: "1.0",
	maxVoiceVolume: "1.0",
	minVoiceVolume: "0.1",
	voiceVolumeStep: "0.1",
	voiceVolumeTooltip : "Громкость речи",

	voiceIdTooltip: "Выбор голоса",

	useAITooltip: "Возможны ошибки и нестабильности! Гораздо более долгое время обработки! Только английский язык!",
};

export default App;
export {TTSForm};
