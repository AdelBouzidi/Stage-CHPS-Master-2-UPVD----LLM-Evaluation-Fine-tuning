program palindrome_changes
  implicit none
  integer, parameter :: max_len = 1000
  integer :: arr_len
  integer, allocatable :: arr(:)
  integer :: i, changes
  
  ! Read array length
  read(*,*) arr_len
  
  ! Read array elements
  allocate(arr(arr_len))
  do i = 1, arr_len
    read(*,*) arr(i)
  end do
  
  ! Count changes needed
  changes = 0
  do i = 1, arr_len/2
    if (arr(i) /= arr(arr_len - i + 1)) then
      changes = changes + 1
    end if
  end do
  
  ! Output result
  print*, changes
  
  deallocate(arr)
  
end program palindrome_changes