package com.example.myapplication.fragment

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.core.os.bundleOf
import androidx.navigation.NavOptions
import androidx.navigation.Navigation
import androidx.navigation.fragment.findNavController
import com.example.myapplication.R
import com.example.myapplication.databinding.FragmentCustomerFormLossThreeBinding

class CustomerFormLossThreeFragment : Fragment() {

    private var _binding: FragmentCustomerFormLossThreeBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        _binding = FragmentCustomerFormLossThreeBinding.inflate(inflater, container, false)
        binding.btnFormFinal.setOnClickListener {
            val bundle = bundleOf()
            val navOptions: NavOptions = NavOptions.Builder()
                .setPopUpTo(R.id.action_customerFormLossThreeFragment2_to_nav_object_list, true)
                .build()
            Navigation.findNavController(it).navigate(R.id.nav_object_list, bundle, navOptions);
        }
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

       /* binding.buttonFirst.setOnClickListener {
            findNavController().navigate(R.id.action_FirstFragment_to_SecondFragment)
        }*/
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }

}