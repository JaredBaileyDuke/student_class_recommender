import { useState } from "react";
import {
  IconActivity,
  IconActivityHeartbeat,
  IconCurrentLocation,
  IconGenderTransgender,
  IconMoodHappy,
  IconSchool,
} from "@tabler/icons-react";
import axios from "axios";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";

// Local
import countriesJsonList from "./assets/countries.json";
import { LOADER_DURATION, LOADING_STATES } from "./constants";
import { Input } from "./ui/input";
import { MultiStepLoader as Loader } from "./ui/multi-step-loader";
import { Label, LabelInputContainer } from "./ui/label";

function ResponsePreviewComponent({ responseData }) {
  return (
    <div className="m-8 p-8 rounded border-2 shadow-lg">
      <h2 className="text-2xl flex flex-col justify-center items-center mb-8 text-center">
        Course recommendation
      </h2>
      <Markdown remarkPlugins={[remarkGfm]}>{responseData}</Markdown>
    </div>
  );
}

function CustomFormComponent({ setIsLoading, setResponseData }) {
  async function onSubmit(event) {
    event.preventDefault();
    const field_of_study = event.target.field_of_study.value.toString().trim();
    const primary_hobby = event.target.primary_hobby.value.toString().trim();
    const secondary_hobby = event.target.secondary_hobby.value
      .toString()
      .trim();
    const desired_career_field = event.target.desired_career_field.value
      .toString()
      .trim();
    const gender = event.target.gender.value.toString().trim();
    const country_of_origin = event.target.country_of_origin.value
      .toString()
      .trim();

    const requestBody = {
      field_of_study,
      primary_hobby,
      secondary_hobby,
      desired_career_field,
      gender,
      country_of_origin,
    };

    try {
      setIsLoading(true);
      setResponseData(null);
      let response = await axios.post("/recommend-courses/", requestBody);
      response = response.data;
      setResponseData(response);
    } catch (error) {
      alert(error);
      setResponseData(null);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="max-w-md w-full mx-auto rounded-none p-8 shadow-input mb-16 font-light">
      <form onSubmit={onSubmit}>
        <LabelInputContainer className="mb-8">
          <Label htmlFor="field_of_study">
            Field of study&nbsp;
            <IconSchool size={20} />
          </Label>
          <Input
            id="field_of_study"
            placeholder="Computer Science"
            type="text"
          />
        </LabelInputContainer>

        <div className="flex flex-row space-y-2 md:space-y-0 md:space-x-2 mb-8">
          <LabelInputContainer>
            <Label htmlFor="primary_hobby">
              Hobby (primary)&nbsp;
              <IconActivity size={20} />
            </Label>
            <Input id="primary_hobby" placeholder="Reading books" type="text" />
          </LabelInputContainer>

          <LabelInputContainer>
            <Label htmlFor="secondary_hobby">
              Hobby (secondary)&nbsp;
              <IconActivityHeartbeat size={20} />
            </Label>
            <Input id="secondary_hobby" placeholder="Cycling" type="text" />
          </LabelInputContainer>
        </div>

        <LabelInputContainer className="mb-8">
          <Label htmlFor="desired_career_field">
            Desired career&nbsp;
            <IconMoodHappy size={20} />
          </Label>
          <Input
            id="desired_career_field"
            placeholder="Applied Machine Learning Engineer"
            type="text"
          />
        </LabelInputContainer>

        <LabelInputContainer className="mb-8">
          <Label htmlFor="gender">
            Gender&nbsp;
            <IconGenderTransgender size={20} />
          </Label>
          <select id="gender" name="gender">
            <option value="male">Male</option>
            <option value="female">Female</option>
          </select>
        </LabelInputContainer>

        <LabelInputContainer className="mb-4">
          <Label htmlFor="country_of_origin">
            Country of origin&nbsp;
            <IconCurrentLocation size={20} />
          </Label>
          <select id="country_of_origin" name="country_of_origin">
            {countriesJsonList.map((country) => (
              <option key={country.name} value={country.name}>
                {country.name}
              </option>
            ))}
          </select>
        </LabelInputContainer>

        <div className="bg-gradient-to-r from-transparent via-neutral-300 dark:via-neutral-700 to-transparent my-8 h-[1px] w-full" />

        <button
          className="bg-gradient-to-br relative group/btn from-black to-neutral-600 block w-full text-white rounded-md h-10 font-medium shadow-[0px_1px_0px_0px_#ffffff40_inset,0px_-1px_0px_0px_#ffffff40_inset] dark:shadow-[0px_1px_0px_0px_var(--zinc-800)_inset,0px_-1px_0px_0px_var(--zinc-800)_inset]"
          type="submit"
        >
          Sign up &rarr;
          <span className="group-hover/btn:opacity-100 block transition duration-500 opacity-0 absolute h-px w-full -bottom-px inset-x-0 bg-gradient-to-r from-transparent via-cyan-500 to-transparent" />
          <span className="group-hover/btn:opacity-100 blur-sm block transition duration-500 opacity-0 absolute h-px w-1/2 mx-auto -bottom-px inset-x-10 bg-gradient-to-r from-transparent via-indigo-500 to-transparent" />
        </button>
      </form>
    </div>
  );
}

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [responseData, setResponseData] = useState(null);

  return (
    <div>
      <h2 className="font-light text-4xl flex flex-col justify-center items-center m-8 text-center">
        Duke Grad Student Course Recommender
      </h2>
      <CustomFormComponent
        setIsLoading={setIsLoading}
        setResponseData={setResponseData}
      />
      <Loader
        loadingStates={LOADING_STATES}
        loading={isLoading}
        duration={LOADER_DURATION}
        loop={false}
      />

      {responseData && <ResponsePreviewComponent responseData={responseData} />}
    </div>
  );
}

export default App;
