package com.example.myapplication.fragment

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.navigation.fragment.findNavController
import androidx.recyclerview.widget.GridLayoutManager
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.myapplication.R
import com.example.myapplication.adapter.ObjectListAdapter
import com.example.myapplication.databinding.FragmentCustomerObjectListBinding
import com.example.myapplication.model.getDataObjects

class CustomerObjectLDetailFragment : Fragment() {

    private var _binding: FragmentCustomerObjectListBinding? = null
    private lateinit var recyclerCustomerObjectList: RecyclerView
    private lateinit var adapter: ObjectListAdapter
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {

        _binding = FragmentCustomerObjectListBinding.inflate(inflater, container, false)
        return binding.root

    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        val linearLayoutManager = LinearLayoutManager(context)
        recyclerCustomerObjectList = binding.recyclerCustomerObjectList
        recyclerCustomerObjectList.layoutManager = linearLayoutManager
        recyclerCustomerObjectList.setHasFixedSize(true)
//        getDataObjects()
        adapter = ObjectListAdapter(
            getDataObjects()
        )
        recyclerCustomerObjectList.adapter = adapter
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}