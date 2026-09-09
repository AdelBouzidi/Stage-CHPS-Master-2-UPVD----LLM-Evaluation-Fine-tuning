program get_odd_collatz_demo
  implicit none
  integer, dimension(:), allocatable :: result
  integer :: n
  
  ! Read input from stdin
  read(*,*) n
  
  ! Call the function
  result = get_odd_collatz(n)
  
  ! Print output to stdout
  print(*,'(i0)') result
contains

  function get_odd_collatz(n) result(res)
    integer, intent(in) :: n
    integer, allocatable :: res(:)
    integer :: i, temp
    integer, dimension(:), allocatable :: temp_arr(:)
    
    ! Generate Collatz sequence and collect odd numbers
    temp = n
    do
      if (mod(temp, 2) == 1) then
        allocate(temp_arr(size(temp_arr)+1))
        temp_arr = [temp_arr, temp]
      end if
      if (temp == 1) exit
      if (mod(temp, 2) == 0) then
        temp = temp / 2
      else
        temp = 3 * temp + 1
      end if
    end do
    
    ! Sort the array
    call sort_array(temp_arr, res)
  end function get_odd_collatz

  subroutine sort_array(arr, sorted)
    integer, intent(in) :: arr(:)
    integer, intent(out) :: sorted(:)
    integer :: i, j, temp
    sorted = arr
    do i = 1, size(sorted)
      do j = 1, size(sorted) - i
        if (sorted(j) > sorted(j+1)) then
          temp = sorted(j)
          sorted(j) = sorted(j+1)
          sorted(j+1) = temp
        end if
      end do
    end do
  end subroutine sort_array

end program get_odd_collatz_demo