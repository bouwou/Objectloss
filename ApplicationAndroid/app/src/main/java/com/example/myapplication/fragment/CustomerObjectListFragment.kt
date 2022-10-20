package com.example.myapplication.fragment

import android.os.Bundle
import android.view.*
import androidx.appcompat.widget.SearchView
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import androidx.recyclerview.widget.GridLayoutManager
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.myapplication.R
import com.example.myapplication.adapter.ObjectListAdapter
import com.example.myapplication.databinding.FragmentCustomerObjectListBinding
import com.example.myapplication.model.getDataObjects

class CustomerObjectListFragment : Fragment() {

    private var _binding: FragmentCustomerObjectListBinding? = null
    private lateinit var recyclerCustomerObjectList: RecyclerView
    private lateinit var adapter: ObjectListAdapter
    private val binding get() = _binding!!

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setHasOptionsMenu(true)
    }

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

    override fun onCreateOptionsMenu(menu: Menu, inflater: MenuInflater) {
        super.onCreateOptionsMenu(menu, inflater)
        inflater.inflate(R.menu.main_activity_drawer, menu)
        var searchItem: MenuItem = menu.findItem(R.id.action_search)
        var searchView: SearchView = searchItem.actionView as SearchView

        searchView.setOnQueryTextListener(object : SearchView.OnQueryTextListener {
            override fun onQueryTextSubmit(p0: kotlin.String?): Boolean {
                println(p0)
                return false
            }

            override fun onQueryTextChange(p0: kotlin.String?): Boolean {
                println(p0)
                adapter.filter.filter(p0)
                return false
            }

        })
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        when (item.itemId) {
            else -> super.onOptionsItemSelected(item)
        }
        return super.onOptionsItemSelected(item)
    }
}