program sum_odd_at_even_positions
  implicit none
  integer :: n, i, sum, value
  integer, allocatable :: arr(:)
  
  ! Read array length
  read(*, *) n
  
  ! Read array elements
  allocate(arr(n))
  do i = 1, n
    read(*, *) arr(i)
  end do
  
  ! Calculate sum of odd elements at even positions
  sum = 0
  do i = 2, n, 2  ! Even positions: 2, 4, 6, ...
    if (mod(arr(i), 2) /= 0) then  ! Odd value
      sum = sum + arr(i)
    end if
  end do
  
  ! Output result
  print *, sum
  
  deallocate(arr)
end program sum_odd_at_even_positions