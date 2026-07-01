// Exercise database for Tendon Isometrics.
// Video IDs point to verified, publicly available YouTube demonstrations from
// physiotherapy / sports-rehab sources. Sourced via web search on 2026-07-01.
const REGIONS = [
  {
    id: "ankle",
    name: "Ankle & Achilles Tendon",
    blurb: "Loads the Achilles tendon and calf-tendon complex.",
    exercises: [
      {
        id: "single-leg-calf-hold",
        name: "Isometric Single-Leg Calf Raise Hold",
        target: "Achilles tendon",
        videoId: "x1LhV2nj01Q",
        secondary: [],
        protocol: "5 x 45s holds, 2-3x/day. Progress from double-leg to single-leg as tolerated.",
        steps: [
          "Stand facing a wall, fingertips on the wall for balance.",
          "Rise onto the ball of one foot (or both feet if single-leg is too hard).",
          "Hold at the top of the raise, knee straight or very slightly bent.",
          "Keep weight through the big toe/second toe, hold steady without wobbling.",
          "Lower under control after the hold and rest before repeating."
        ]
      },
      {
        id: "achilles-isometric-progression",
        name: "Achilles Isometric Holds (Wall / Step Variations)",
        target: "Achilles tendon (mid-portion & insertional)",
        videoId: "isVPZTr5iXk",
        secondary: [],
        protocol: "4 x 40s holds, 2-3x/day, most days of the week during a flare-up.",
        steps: [
          "Choose a position: flat floor for mid-portion pain, or a small step with heel level/slightly raised for insertional pain (avoid deep stretch below the step edge).",
          "Raise onto the ball(s) of the feet to a comfortable height.",
          "Hold the position at a level you can maintain without pain rising above ~3-4/10.",
          "Breathe normally throughout the hold; don't brace or hold your breath.",
          "Lower slowly and rest 60-90s between holds."
        ]
      }
    ]
  },
  {
    id: "knee",
    name: "Knee & Patellar Tendon",
    blurb: "Loads the patellar (and quad) tendon while minimizing joint compression.",
    exercises: [
      {
        id: "spanish-squat",
        name: "Spanish Squat",
        target: "Patellar / quadriceps tendon",
        videoId: "NzBj2XEzySc",
        secondary: ["-ksofnvkohI"],
        protocol: "5 x 45s holds, 2-3x/day (can be used as a pre-activity pain reliever too).",
        steps: [
          "Loop a heavy resistance band around the back of both knees and anchor it to a solid, stable post at knee height.",
          "Step back until there is firm tension in the band.",
          "Sit back into the band, keeping shins near-vertical and trunk upright, knees bending to roughly 60-90 degrees.",
          "Hold the position, letting the band support you so quads work isometrically without extra knee-joint compression.",
          "Push back up to standing to finish the hold."
        ]
      }
    ]
  },
  {
    id: "elbow",
    name: "Elbow Tendons",
    blurb: "Covers both the outside (extensor) and inside (flexor) elbow tendons.",
    exercises: [
      {
        id: "isometric-wrist-extension",
        name: "Isometric Wrist Extension (Tennis Elbow)",
        target: "Common extensor tendon / lateral epicondyle",
        videoId: "3VboWPSJ7Pw",
        secondary: ["NxWE5ocZr8s"],
        protocol: "5 x 30-45s holds, 1-2x/day.",
        steps: [
          "Rest your forearm palm-down on a table with your wrist hanging just off the edge, or press the back of your hand against the underside of a table.",
          "Use your other hand (or the table) to resist as you try to lift/extend your wrist upward.",
          "Hold firm, even pressure without any wrist movement.",
          "Keep the elbow relaxed and pain during the hold at a tolerable level (≤3-4/10).",
          "Release slowly and rest before the next hold."
        ]
      },
      {
        id: "isometric-wrist-flexion",
        name: "Isometric Wrist Flexion (Golfer's Elbow)",
        target: "Common flexor tendon / medial epicondyle",
        videoId: "jSX3SJwFv20",
        secondary: [],
        protocol: "5 x 30-45s holds, 1-2x/day.",
        steps: [
          "Rest your forearm palm-up on a table or your thigh, wrist just off the edge.",
          "Place your other hand across your palm/fingers to provide resistance.",
          "Try to flex the wrist upward into your resisting hand without allowing any movement.",
          "Hold steady, even pressure, keeping the elbow relaxed.",
          "Release slowly and rest between holds."
        ]
      }
    ]
  },
  {
    id: "shoulder",
    name: "Shoulder Tendons",
    blurb: "Targets the rotator cuff and the long head of the biceps tendon.",
    exercises: [
      {
        id: "isometric-shoulder-external-rotation",
        name: "Isometric Shoulder External Rotation",
        target: "Rotator cuff (infraspinatus / teres minor)",
        videoId: "ozhHe-u6uMM",
        secondary: [],
        protocol: "5 x 20-45s holds (or shorter 5-10s holds x10 if very irritable), 1-2x/day.",
        steps: [
          "Stand in a doorway or next to a wall, elbow bent to 90 degrees and tucked at your side.",
          "Place the back of your wrist against the door frame/wall.",
          "Press your hand outward into the frame without letting your arm actually move.",
          "Hold the tension, keeping the shoulder blade relaxed and down.",
          "Release slowly and repeat on the same side."
        ]
      },
      {
        id: "isometric-biceps-tendon-hold",
        name: "Isometric Biceps Tendon Hold",
        target: "Long head of biceps tendon",
        videoId: "JNXc7gIieKI",
        secondary: ["rG6hFwdZVhg"],
        protocol: "5 x 30-45s holds, 1x/day, progressing hold time/angle as tolerated.",
        steps: [
          "Bend the elbow to about 90 degrees, palm facing up.",
          "Brace your forearm against a table edge, doorframe, or your other hand.",
          "Push your forearm upward into the resistance without letting the elbow move.",
          "Hold steady tension, keeping the shoulder relaxed and down away from your ear.",
          "Release slowly and rest before repeating."
        ]
      }
    ]
  },
  {
    id: "hip",
    name: "Hip & Groin Tendons",
    blurb: "Covers the gluteal, adductor, and proximal hamstring tendons.",
    exercises: [
      {
        id: "isometric-hip-abduction",
        name: "Isometric Hip Abduction (Side-Lying or Standing)",
        target: "Gluteal tendon (gluteus medius/minimus)",
        videoId: "d0480UMDFZo",
        secondary: [],
        protocol: "4-5 x 30-45s holds, most days during a flare-up; keep loads low and avoid hip-hitching.",
        steps: [
          "Standing option: stand side-on to a wall, about a foot away, and press the outside of your ankle into the wall.",
          "Side-lying option: lie on your unaffected side with a pillow between your knees, top hip in a neutral (not adducted) position.",
          "Gently push the leg outward/into the wall without letting the pelvis hike up or rotate.",
          "Hold at a low-to-moderate effort — avoid pushing into a painful pinching sensation at the hip.",
          "Release slowly and rest between holds."
        ]
      },
      {
        id: "isometric-adductor-squeeze",
        name: "Isometric Adductor Squeeze",
        target: "Adductor tendon (groin)",
        videoId: "G3HeujBhXqY",
        secondary: [],
        protocol: "3-5 x 20-60s holds, daily during acute groin pain.",
        steps: [
          "Lie on your back with both knees bent, feet flat on the floor.",
          "Place a ball, pillow, or foam block between your knees.",
          "Squeeze your knees together into the ball at a comfortable, controlled effort.",
          "Hold steady without pain spiking above a tolerable level.",
          "Relax slowly and rest before repeating."
        ]
      },
      {
        id: "isometric-hamstring-bridge",
        name: "Isometric Hamstring Bridge Hold",
        target: "Proximal hamstring tendon",
        videoId: "BquK5pHIcrk",
        secondary: [],
        protocol: "4-5 x 45s holds, up to 3x/day for the first 1-2 weeks, then progress to loaded isotonic work.",
        steps: [
          "Lie on your back with knees bent, feet flat, hip-width apart.",
          "Drive through your heels to lift your hips into a bridge position.",
          "Hold at the top with a flat/neutral pelvis, squeezing the glutes and hamstrings.",
          "Keep the hold pain-free or only mildly uncomfortable at the sit bone area.",
          "Lower slowly and rest before the next hold."
        ]
      }
    ]
  }
];
